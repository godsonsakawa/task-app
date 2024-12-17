from rest_framework import permissions

class IsUserOwnerOrGetAndPostOnly(permissions.BasePermission):
    """
    Custom permissions for UserViewSet to restrict access based on user ownership.

    This permission class allows:
    - GET requests for all users.
    - POST requests for all users to create new users.
    - PUT, PATCH, or DELETE requests only for the user who owns the account.

    Method Behavior:
        - has_permission: Grants permission to all requests.
        - has_object_permission: Grants permission for safe methods (GET, HEAD, OPTIONS) 
          and allows editing (PUT, PATCH, DELETE) only for the user who owns the object.

    Attributes:
        request (Request): The request object.
        view (View): The view that is being accessed.
        obj (User): The user object being accessed or modified.
    """

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if not request.user.is_anonymous:
            return request.user == obj

        return False


class IsProfileOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permissions for ProfileViewSet to restrict access based on profile ownership.

    This permission class allows:
    - GET requests for all users.
    - POST requests for all users to create new profiles.
    - PUT, PATCH, or DELETE requests only for the user who owns the profile.

    Method Behavior:
        - has_permission: Grants permission to all requests.
        - has_object_permission: Grants permission for safe methods (GET, HEAD, OPTIONS) 
          and allows editing (PUT, PATCH, DELETE) only for the user who owns the profile.

    Attributes:
        request (Request): The request object.
        view (View): The view that is being accessed.
        obj (Profile): The profile object being accessed or modified.
    """

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        if not request.user.is_anonymous:
            return request.user.profile == obj
        
        return False