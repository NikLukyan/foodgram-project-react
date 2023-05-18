from rest_framework import permissions


class IsAuthorOrAdminOrReadOnly(permissions.BasePermission):
    message = 'Редактирование чужого рецепта запрещено!'

    def has_object_permission(self, request, view, obj):
        return bool(request.method in permissions.SAFE_METHODS
                    or obj.author == request.user
                    or request.user.is_superuser)
