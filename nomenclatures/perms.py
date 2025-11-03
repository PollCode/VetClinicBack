from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied
from accounts.models.users import User


class HasAddAreaPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if not hasattr(request.user, 'rol') or not request.user.rol:
            raise PermissionDenied(
                'Tu cuenta no tiene asignado un rol. Contacta al administrador.')

        # Permitir acceso si el usuario es administrador o superusuario
        if request.user.rol == User.Role.ADMINISTRADOR.value or request.user.is_superuser:
            return True

        raise PermissionDenied('No tienes permiso para agregar áreas.')


class HasChangeAreaPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if not hasattr(request.user, 'rol') or not request.user.rol:
            raise PermissionDenied(
                'Tu cuenta no tiene asignado un rol. Contacta al administrador.')

       # Permitir acceso si el usuario es administrador o superusuario
        if request.user.rol == User.Role.ADMINISTRADOR.value or request.user.is_superuser:
            return True

        raise PermissionDenied('No tienes permiso para modificar áreas.')


class HasViewAreaPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if not hasattr(request.user, 'rol') or not request.user.rol:
            raise PermissionDenied(
                'Tu cuenta no tiene asignado un rol. Contacta al administrador.')

        # Permitir acceso si el usuario es administrador o superusuario
        if request.user.rol == User.Role.ADMINISTRADOR.value or request.user.is_superuser:
            return True

        raise PermissionDenied('No tienes permiso para ver áreas.')


class HasDeleteAreaPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if not hasattr(request.user, 'rol') or not request.user.rol:
            raise PermissionDenied(
                'Tu cuenta no tiene asignado un rol. Contacta al administrador.')

        # Permitir acceso si el usuario es administrador o superusuario
        if request.user.rol == User.Role.ADMINISTRADOR.value or request.user.is_superuser:
            return True

        raise PermissionDenied('No tienes permiso para eliminar áreas.')



class HasAddSpeciesPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if not hasattr(request.user, 'rol') or not request.user.rol:
            raise PermissionDenied(
                'Tu cuenta no tiene asignado un rol. Contacta al administrador.')

        # Permitir acceso si el usuario es administrador o superusuario
        if request.user.rol == User.Role.ADMINISTRADOR.value or request.user.is_superuser:
            return True

        raise PermissionDenied('No tienes permiso para agregar especies.')


class HasChangeSpeciesPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if not hasattr(request.user, 'rol') or not request.user.rol:
            raise PermissionDenied(
                'Tu cuenta no tiene asignado un rol. Contacta al administrador.')

       # Permitir acceso si el usuario es administrador o superusuario
        if request.user.rol == User.Role.ADMINISTRADOR.value or request.user.is_superuser:
            return True

        raise PermissionDenied('No tienes permiso para modificar especies.')


class HasViewSpeciesPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if not hasattr(request.user, 'rol') or not request.user.rol:
            raise PermissionDenied(
                'Tu cuenta no tiene asignado un rol. Contacta al administrador.')

        # Permitir acceso si el usuario es administrador o superusuario
        if request.user.rol == User.Role.ADMINISTRADOR.value or request.user.is_superuser:
            return True

        raise PermissionDenied('No tienes permiso para ver especies.')


class HasDeleteSpeciesPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if not hasattr(request.user, 'rol') or not request.user.rol:
            raise PermissionDenied(
                'Tu cuenta no tiene asignado un rol. Contacta al administrador.')

        # Permitir acceso si el usuario es administrador o superusuario
        if request.user.rol == User.Role.ADMINISTRADOR.value or request.user.is_superuser:
            return True

        raise PermissionDenied('No tienes permiso para eliminar especies.')
    
    
class HasAddBreedPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if not hasattr(request.user, 'rol') or not request.user.rol:
            raise PermissionDenied(
                'Tu cuenta no tiene asignado un rol. Contacta al administrador.')

        # Permitir acceso si el usuario es administrador o superusuario
        if request.user.rol == User.Role.ADMINISTRADOR.value or request.user.is_superuser:
            return True

        raise PermissionDenied('No tienes permiso para agregar razas.')


class HasChangeBreedPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if not hasattr(request.user, 'rol') or not request.user.rol:
            raise PermissionDenied(
                'Tu cuenta no tiene asignado un rol. Contacta al administrador.')

       # Permitir acceso si el usuario es administrador o superusuario
        if request.user.rol == User.Role.ADMINISTRADOR.value or request.user.is_superuser:
            return True

        raise PermissionDenied('No tienes permiso para modificar razas.')


class HasViewBreedPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if not hasattr(request.user, 'rol') or not request.user.rol:
            raise PermissionDenied(
                'Tu cuenta no tiene asignado un rol. Contacta al administrador.')

        # Permitir acceso si el usuario es administrador o superusuario
        if request.user.rol == User.Role.ADMINISTRADOR.value or request.user.is_superuser:
            return True

        raise PermissionDenied('No tienes permiso para ver razas.')


class HasDeleteBreedPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if not hasattr(request.user, 'rol') or not request.user.rol:
            raise PermissionDenied(
                'Tu cuenta no tiene asignado un rol. Contacta al administrador.')

        # Permitir acceso si el usuario es administrador o superusuario
        if request.user.rol == User.Role.ADMINISTRADOR.value or request.user.is_superuser:
            return True

        raise PermissionDenied('No tienes permiso para eliminar razas.')