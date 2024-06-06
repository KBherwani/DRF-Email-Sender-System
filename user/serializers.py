from datetime import date

from django.utils import timezone
from rest_framework import serializers

from .models import EmailSchedule, User


class UserCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new user instance.

    Attributes:
        model: The User model class.
        fields: The fields to include in the serialized output.

    Methods:
        validate_email: Check that the email is not already in use.
        validate_phone_number: Check that the phone number is valid.
        validate: Perform additional validation on the entire set of data.
    """

    class Meta:
        model = User
        fields = ["name", "email", "phone_number", "date_of_birth"]

    def validate_email(self, value):
        """
        Check that the email is not already in use.
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value

    def validate_phone_number(self, value):
        """
        Check that the phone number is valid.
        """
        if not value.isdigit():
            raise serializers.ValidationError("Phone number must contain only digits.")
        if len(value) < 10:
            raise serializers.ValidationError(
                "Phone number must be at least 10 digits long."
            )
        return value

    def validate(self, data):
        """
        Perform additional validation on the entire set of data.
        """
        if data["date_of_birth"] > date.today():
            raise serializers.ValidationError("Date of birth cannot be in the future.")
        return data


class UserDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying detailed information about a user instance.

    Attributes:
        model: The User model class.
        fields: The fields to include in the serialized output.
    """

    class Meta:
        model = User
        fields = ["id", "name", "email", "phone_number", "date_of_birth"]


class EmailScheduleCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new email schedule instance.

    Attributes:
        model: The EmailSchedule model class.
        fields: The fields to include in the serialized output.

    Methods:
        validate_scheduled_time: Check that the scheduled time is in the future.
        validate_scheduled_date: Check that the scheduled date is in the future.
    """

    class Meta:
        model = EmailSchedule
        fields = ["user", "scheduled_time", "scheduled_date"]

    def validate_scheduled_time(self, value):
        """
        Check that the scheduled time is in the future.
        """
        if self.initial_data["scheduled_date"] == str(timezone.now().date()):
            if value <= timezone.now().time():
                raise serializers.ValidationError(
                    "The scheduled time must be in the future."
                )
        return value

    def validate_scheduled_date(self, value):
        """
        Check that the scheduled date is in the future.
        """
        if value < timezone.now().date():
            raise serializers.ValidationError(
                "The scheduled date must be in the future."
            )
        return value


class EmailScheduleDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying detailed information about an email schedule instance.

    Attributes:
        model: The EmailSchedule model class.
        fields: The fields to include in the serialized output.
    """

    user = UserDetailSerializer()

    class Meta:
        model = EmailSchedule
        fields = ["id", "user", "scheduled_time", "scheduled_date", "email_status"]
