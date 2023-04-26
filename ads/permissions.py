from rest_framework.permissions import BasePermission

from users.models import User


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'owner'):
            owner = obj.owner
        elif hasattr(obj, 'author'):
            owner = obj.author
        else:
            return False
        if request.user == obj.owner:
            return True


class IsStuff(BasePermission):
    def has_permission(self, request, view):
        if request.user.role in ['admin', 'moderator']:
            return True
        return False
