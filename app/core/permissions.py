from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated, BasePermission
from django.contrib.auth.models import User

class UpdateOwnProfile(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.id == request.user.id

class IsResearcher(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.groups.filter(name='RESEARCHER').exists()

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.groups.filter(name='ADMIN').exists()

class IsPrincipalManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.groups.filter(name='PRINCIPALMANAGER').exists()

class IsAllocationManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.groups.filter(name='ALLOCATIONMANAGER').exists()

class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.groups.filter(name='STUDENT').exists()

class IsAdminOrIsStudent(BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and (request.user.groups.filter(name='ADMIN').exists()
                     or request.user.groups.filter(name='STUDENT').exists()))

class IsAdminOrIsResearcher(BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and (request.user.groups.filter(name='ADMIN').exists()
                     or request.user.groups.filter(name='RESEARCHER').exists()))

class IsAdminOrIsPrincipalManager(BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and (request.user.groups.filter(name='ADMIN').exists()
                     or request.user.groups.filter(name='PRINCIPALMANAGER').exists()))

class IsAdminOrIsAllocationManager(BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and (request.user.groups.filter(name='ADMIN').exists()
                     or request.user.groups.filter(name='ALLOCATIONMANAGER').exists()))

class IsAllocationManagerOrIsStudentOrIsResearcher(BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and (request.user.groups.filter(name='RESEARCHER').exists()
                     or request.user.groups.filter(name='ALLOCATIONMANAGER').exists()
                     or request.user.groups.filter(name='STUDENT').exists()))

class IsStudentOrResearcher(BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and (request.user.groups.filter(name='STUDENT').exists()
                     or request.user.groups.filter(name='RESEARCHER').exists()))
