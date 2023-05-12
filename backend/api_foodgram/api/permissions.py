from rest_framework import permissions


class AdminAllOnlyAuthorPermission(permissions.BasePermission):
    """
    Кастомный пермишен для работы администратора и
    автора объекта с небезопасными методами.
    """
    def has_object_permission(self, request, view, obj):
        """Определяем права на уровне объекта."""
        return bool(
            request.user.is_superuser
            or obj.author == request.user
            or request.user.groups.filter(name='recipes_admins').exists()
        )


class IsAuthorOrReadOnly(permissions.BasePermission):
    message = 'Редактирование чужого рецепта запрещено!'

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user)


class IsAdminOrReadOnly(permissions.BasePermission):
    message = 'Редактировать контент может только администратор!'

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS or request.user.is_staff
        )
