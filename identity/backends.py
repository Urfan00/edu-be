from django.contrib.auth.backends import BaseBackend, ModelBackend
from django.contrib.auth.models import Permission


class CustomBaseBackend(BaseBackend):
    """
    Base backend that handles user, group, and role permissions.
    """

    def get_role_permissions(self, user_obj, obj=None):
        return set()

    def get_all_permissions(self, user_obj, obj=None):
        return {
            *self.get_user_permissions(user_obj, obj=obj),
            *self.get_group_permissions(user_obj, obj=obj),
            *self.get_role_permissions(user_obj, obj=obj),
        }


class CustomModelBackend(CustomBaseBackend, ModelBackend):
    """
    Custom authentication backend that extends ModelBackend to include role-based permissions.
    Authenticates against settings.AUTH_USER_MODEL and checks for role-based permissions.
    """

    def _get_permissions(self, user_obj, obj, from_name):
        """
        Return the permissions of `user_obj` from `from_name`. `from_name` can
        be either "group", "user", or "role" to return permissions from
        `_get_group_permissions`, `_get_user_permissions`, or `_get_role_permissions` respectively.
        """
        return super()._get_permissions(user_obj, obj, from_name)

    def _get_role_permissions(self, user_obj):
        roles = user_obj.roles.all()
        return Permission.objects.filter(role__in=roles)

    def get_role_permissions(self, user_obj, obj=None):
        """
        Return a set of permission strings the user `user_obj` has from the
        roles they belong to.
        """
        return self._get_permissions(user_obj, obj, "role")
