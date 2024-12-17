from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the Profile model.

    This serializer converts Profile model instances to and from JSON format,
    allowing for easy interaction with the API. It includes a hyperlink to the 
    associated User instance and supports basic serialization and deserialization 
    of profile data.

    Attributes:
        user (HyperlinkedRelatedField): A read-only field that provides a hyperlink 
        to the related User instance. This field is not editable and uses the 
        'user-detail' view to generate the hyperlink.

    Meta:
        model (Profile): The model that this serializer is associated with.
        fields (list): A list of fields to include in the serialized output. 
        This includes:
            - 'url': The API endpoint for the Profile instance.
            - 'id': The unique identifier for the Profile.
            - 'user': A hyperlink to the associated User instance.
            - 'image': The profile image associated with the Profile.
    """
    
    user = serializers.HyperlinkedRelatedField(read_only=True, many=False, view_name='user-detail')

    class Meta:
        model = Profile
        fields = ['url', 'id', 'user', 'image']



class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.

    This serializer handles the serialization and deserialization of User model instances. 
    It is designed to facilitate interactions with the API while ensuring that sensitive 
    information, such as the password, is managed securely.

    Attributes:
        password (CharField): A write-only field for the user's password. 
        This field is required only during user creation or updates, and it will not be 
        included in the serialized output.
        
        old_password (CharField): A write-only field for the user's old password, 
        required during an update when changing the password.
        
        username (CharField): A read-only field that provides the username of the user.
        
        profile (ProfileSerializer): A read-only field that represents the associated 
        Profile instance of the user, serialized using the ProfileSerializer.

    Meta:
        model (User): The model that this serializer is associated with.
        fields (list): A list of fields to include in the serialized output, including:
            - 'url': The API endpoint for the User instance.
            - 'id': The unique identifier for the User.
            - 'username': The username of the User.
            - 'email': The email address of the User.
            - 'first_name': The first name of the User.
            - 'last_name': The last name of the User.
            - 'password': The password for the User (write-only).
            - 'profile': The associated Profile instance data.
    """

    password = serializers.CharField(write_only=True, required=False)
    old_password = serializers.CharField(write_only=True, required=False)
    username = serializers.CharField(read_only=True)
    profile = ProfileSerializer(read_only=True)

    def validate(self, data):
        """
        Validate the input data for user creation and updates.

        This method ensures that the required fields are present based on the request method:
        - For POST requests, the password must be provided.
        - For PUT or PATCH requests, if a new password is provided, the old password must also be supplied.

        Args:
            data (dict): The input data to validate.

        Raises:
            serializers.ValidationError: If validation fails, with a message indicating the issue.

        Returns:
            dict: The validated data if all checks pass.
        """
        request_method = self.context['request'].method
        password = data.get('password', None)
        if request_method == 'POST':
            if password is None:
                raise serializers.ValidationError({"info": "Please provide a password."})
        elif request_method in ['PUT', 'PATCH']:
            old_password = data.get('old_password', None)
            if password is not None and old_password is None:
                raise serializers.ValidationError({"info": "Please provide the old password."})
        return data

    def create(self, validated_data):
        """
        Create a new user instance.

        This method takes validated data, extracts the password, 
        creates a new user with the provided data, sets the user 
        password securely, and saves the user instance to the database.

        Args:
            validated_data (dict): A dictionary containing validated user data.
                Expected keys include all required user fields except 'password'.

        Returns:
            User: The created user instance.
        """
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()

        return user

    def update(self, instance, validated_data):
        """
        Update an existing user instance.

        This method updates the user data, including changing the password if provided 
        and verified against the old password.

        Args:
            instance (User): The user instance to update.
            validated_data (dict): A dictionary containing validated user data.

        Raises:
            serializers.ValidationError: If the old password does not match.

        Returns:
            User: The updated user instance.
        """
        try:
            user = instance
            if 'password' in validated_data:
                password = validated_data.pop('password')
                old_password = validated_data.pop('old_password')
                if user.check_password(old_password):
                    user.set_password(password)
                else:
                    raise Exception("Old password is incorrect.")
                user.save()
        except Exception as err:
            raise serializers.ValidationError({"info": str(err)})
        return super(UserSerializer, self).update(instance, validated_data)

    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'email', 'first_name', 
                  'last_name', 'password', 'old_password', 'profile']


