from rest_framework import permissions
from django.core.exceptions import ValidationError, PermissionDenied


class IsOwnerOrReadOnly(permissions.BasePermission):
  def has_object_permission(self, request, view, obj):
    if request.method in permissions.SAFE_METHODS:
      return True
    return obj.owner == request.user

class HasMoviePermissions(permissions.BasePermission):
  def has_object_permission(self, request, view, obj):
    user=request.user
    if request.method in permissions.SAFE_METHODS:
      return True
    return user.groups.filter(name='Movie Curator').exists()

class IsCuratorOrReadOnly(permissions.BasePermission):
  def has_permission(self, request, view):
    print(view.serializer_class)
    user=request.user
    if user.groups.filter(name='Movie Curator').exists():
      return True
    else:
      PermissionDenied("Not a curator")