import os
from django.db import models
from django.contrib.auth.models import User
from django.utils.deconstruct import deconstructible

@deconstructible
class GenerateProfileImagePath(object):
    """
    A callable class that generates a file path for user profile images.

    This class is used to define a custom upload path for profile images associated 
    with user accounts. It ensures that each user's profile image is stored in a 
    unique directory based on their user ID.

    Method:
        __call__(instance, filename): Generates the upload path for the profile image.

    Attributes:
        instance (Profile): The instance of the Profile model.
        filename (str): The original filename of the uploaded image.

    Returns:
        str: The complete file path where the profile image will be stored.
    """

    def __init__(self):
        pass

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]  # Get the file extension
        path = f'media/accounts/{instance.user.id}/images/'  # Define the path
        name = f'profile_image.{ext}'  # Define the image name
        return os.path.join(path, name)  # Return the full path


user_profile_image_path = GenerateProfileImagePath()


class Profile(models.Model):
    """
    A model representing a user profile.

    The Profile model extends the User model with additional information, allowing 
    users to have a profile image. Each profile is linked to a single User instance 
    via a one-to-one relationship.

    Attributes:
        user (OneToOneField): The user associated with this profile.
        image (FileField): The profile image of the user, stored using a custom upload path.

    Methods:
        __str__(): Returns a string representation of the profile, including the username.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.FileField(upload_to=user_profile_image_path, blank=True, null=True)

    def __str__(self):
        return f'{self.user.username}\'s Profile'