from rest_framework.permissions import BasePermission


class IsPostAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated and request.user == obj.author:
            return True
        else:
            return False