from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver  # decorator

from .models import Profile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Create a Profile instance after a User is created.

    This receiver listens for the `post_save` signal emitted by the User model.
    When a new User is created, a corresponding Profile instance is created 
    and associated with the User.

    Args:
        sender (Model): The model class that sent the signal.
        instance (User): The User instance that was created.
        created (bool): A boolean indicating whether a new record was created.
        **kwargs: Additional keyword arguments.
    """
    if created:
        Profile.objects.create(user=instance)


@receiver(pre_save, sender=User)
def set_username(sender, instance, **kwargs):
    """
    Set a unique username for the User before saving.

    This receiver listens for the `pre_save` signal emitted by the User model.
    If the username field is empty, it generates a username based on the user's 
    first and last names. If a username already exists, it appends a counter 
    to make the username unique.

    Args:
        sender (Model): The model class that sent the signal.
        instance (User): The User instance about to be saved.
        **kwargs: Additional keyword arguments.
    """
    if not instance.username:
        username = f'{instance.first_name}_{instance.last_name}'.lower()
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f'{instance.first_name}_{instance.last_name}_{counter}'.lower()
            counter += 1
        instance.username = username