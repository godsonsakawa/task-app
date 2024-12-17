from django.contrib import admin
from .models import Profile

# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for the Profile model.

    This class customizes the admin interface for the Profile model,
    allowing for specific behaviors and settings.

    Attributes:
        readonly_fields (tuple): A tuple of fields that should be read-only in the admin interface.
        In this case, the 'id' field is set to be read-only.
    """
    readonly_fields = ('id',)

# Register the Profile model with the custom ProfileAdmin class.
admin.site.register(Profile, ProfileAdmin)