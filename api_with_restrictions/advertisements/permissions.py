from rest_framework import permissions

class IsCreatorOrReadOnly(permissions.BasePermission):
    message = "Изменять и удалять объявление может только его создатель."

    def has_object_permission(self, request, view, obj):
        # Читать могут все (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True

        # Изменять и удалять может только автор
        return obj.creator == request.user