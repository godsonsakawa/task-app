from django.contrib.auth.models import User
from rest_framework import viewsets, mixins
from .serializers import UserSerializer, ProfileSerializer
from .permissions import IsUserOwnerOrGetAndPostOnly, IsProfileOwnerOrReadOnly
from .models import Profile


class UserViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing User instances.

    This viewset provides the standard actions for the User model:
    - List all users.
    - Retrieve a specific user.
    - Create a new user.
    - Update an existing user.
    - Delete a user.

    Permissions:
        - IsUserOwnerOrGetAndPostOnly: Users can only edit their own account.
          All users can view and create accounts.

    Attributes:
        queryset (QuerySet): The queryset of User instances.
        serializer_class (Serializer): The serializer used to validate and serialize User data.
    """
    permission_classes = [IsUserOwnerOrGetAndPostOnly]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProfileViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.UpdateModelMixin):
    """
    A viewset for retrieving and updating Profile instances.

    This viewset provides the following actions for the Profile model:
    - Retrieve a specific profile.
    - Update the current user's profile.

    Permissions:
        - IsProfileOwnerOrReadOnly: Users can only edit their own profile.
          All users can view profiles.

    Attributes:
        queryset (QuerySet): The queryset of Profile instances.
        serializer_class (Serializer): The serializer used to validate and serialize Profile data.
    """
    permission_classes = [IsProfileOwnerOrReadOnly]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer