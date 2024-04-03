from rest_framework import permissions
import copy


class IsAdminOrReadonly(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.method in permissions.SAFE_METHODS
                    or (request.user and request.user.is_staff))


class SendPrivetEmailToCustomerPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.has_perm('store.send_privet_email')


class CustomDjangoModelPermission(permissions.DjangoModelPermissions):
    def __init__(self) -> None:
        self.perms_map = copy.deepcopy(self.perms_map)
        self.perms_map['GET'] = ['%(app_label)s.view_%(model_name)s']
