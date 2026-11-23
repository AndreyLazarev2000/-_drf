from django.contrib.auth.models import User
from rest_framework import serializers

from advertisements.models import Advertisement, AdvertisementStatusChoices

class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(read_only=True)

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator', 'status', 'created_at',)

    def create(self, validated_data):
        """Метод для создания"""
        # Простановка значения поля создатель по-умолчанию.
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""

        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return data

        # Определяем, какой статус будет у объявления
        # Если при обновлении статус не передан, берем текущий статус объявления
        new_status = data.get(
            "status",
            self.instance.status if self.instance else AdvertisementStatusChoices.OPEN
        )

        # Если объявление открытое, проверяем лимит в 10 штук
        if new_status == AdvertisementStatusChoices.OPEN:
            open_ads = Advertisement.objects.filter(
                creator=request.user,
                status=AdvertisementStatusChoices.OPEN
            )

            # При обновлении (PUT/PATCH) исключаем текущее объявление из подсчета
            if self.instance is not None:
                open_ads = open_ads.exclude(pk=self.instance.pk)

            if open_ads.count() >= 10:
                raise serializers.ValidationError(
                    "У пользователя не может быть больше 10 открытых объявлений."
                )

        return data