import uuid

from django.db import models


class Activity(models.Model):
    """
    This module will contain activity records of each module.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True


class User(Activity):
    """
    Model representing a user with basic personal information.

    Attributes:
    name (str): The user's name, limited to 100 characters.
    email (str): The user's email address, unique.
    phone_number (str, optional): The user's phone number, limited to 15 characters, can be blank.
    date_of_birth (datetime.date, optional): The user's date of birth, can be blank.

    Meta:
    verbose_name (str): Singular name for the model.
    verbose_name_plural (str): Plural name for the model.
    db_table (str): Database table name for the model.
    """

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        db_table = "users"


class EmailSchedule(Activity):
    """
    Model representing an email schedule associated with a user.

    Attributes:
    user (User): The user associated with the email schedule.
    scheduled_time (datetime.time): The time at which the email is scheduled to be sent.
    scheduled_date (datetime.date): The date on which the email is scheduled to be sent.
    email_status (str): The status of the email schedule, chosen from predefined choices.

    Meta:
    verbose_name (str): Singular name for the model.
    verbose_name_plural (str): Plural name for the model.
    db_table (str): Database table name for the model.

    Example usage:
    email_schedule = EmailSchedule.objects.get(pk=1)
    print(email_schedule.scheduled_time) # Output: 08:00:00
    """

    STATUS_CHOICES = (
        ("Pending", "Pending"),
        ("Done", "Done"),
        ("Failed", "Failed"),
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="email_schedules"
    )
    scheduled_time = models.TimeField()
    scheduled_date = models.DateField()
    email_status = models.CharField(
        max_length=50, choices=STATUS_CHOICES, default="Pending"
    )

    def __str__(self):
        return str(self.user.name)

    class Meta:
        verbose_name = "EmailSchedule"
        verbose_name_plural = "EmailSchedules"
        db_table = "email_schedules"
