from django_filters import rest_framework as filters

from advertisements.models import Advertisement


class AdvertisementFilter(filters.FilterSet):
    """Фильтры для объявлений."""

    # Задаем фильтр по диапазону дат для поля created_at
    # Это создаст параметры created_at_after и created_at_before,
    # которые мы видели на твоем первом скриншоте
    created_at = filters.DateFromToRangeFilter()

    class Meta:
        model = Advertisement
        # Указываем, что по полю status можно фильтровать (например, ?status=OPEN)
        fields = ['status']