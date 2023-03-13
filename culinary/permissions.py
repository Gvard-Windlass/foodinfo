from rest_framework import permissions


class HasAccessOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        # if owner of object or staff
        if request.method == "PUT" or request.method == "DELETE":
            return bool(
                request.user == obj.user or request.user and request.user.is_staff
            )

        return False


class HasAccess(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(
            request.user == obj.user
            or request.user
            and request.user.is_staff
            or obj.user.is_staff
        )


class IsStaffOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS
            or request.user
            and request.user.is_staff
        )
