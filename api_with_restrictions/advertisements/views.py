from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend

# Импортируем нашу модель, сериализатор, фильтр и созданные права
from advertisements.models import Advertisement
from advertisements.serializers import AdvertisementSerializer
from advertisements.filters import AdvertisementFilter
from advertisements.permissions import IsCreatorOrReadOnly


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    # Заполняем TODO: настраиваем кверисет, сериализатор и фильтры
    queryset = Advertisement.objects.all().order_by('-created_at')
    serializer_class = AdvertisementSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdvertisementFilter

    def get_permissions(self):
        """Получение прав для действий."""
        # Действия, которые изменяют данные (создание, редактирование, удаление)
        if self.action in ["create", "update", "partial_update", "destroy"]:
            # Требуем авторизацию и проверяем, что это автор объявления
            return [IsAuthenticated(), IsCreatorOrReadOnly()]

        # На чтение (list, retrieve) пускаем всех (AllowAny)
        return [AllowAny()]