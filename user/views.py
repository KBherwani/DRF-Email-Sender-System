"""
The following file is part of the Django web framework and contains the views for your web application.
The file defines view functions or classes that handle the incoming HTTP requests and generate the HTTP responses.
Each view encapsulates the logic for processing requests, such as retrieving data from the database,
performing calculations, and rendering templates or returning data in various formats (e.g., JSON, HTML).
"""

from datetime import datetime, timedelta

from django.conf import settings
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from user.tasks import send_scheduled_email
from utils.custom_response import APIResponse

from .models import EmailSchedule, User
from .serializers import (
    EmailScheduleCreateSerializer,
    EmailScheduleDetailSerializer,
    UserCreateSerializer,
    UserDetailSerializer,
)


class UserAPIView(APIView):
    """
    API view to handle CRUD operations for users.

    Methods:
        get: Handles GET requests to list users or retrieve a specific user.
        post: Handles POST requests to create a new user.
        delete: Handles DELETE requests to delete a specific user.

    Raises:
        LazySettingsException: If there is an exception related to lazy settings.
        Exception: If there is an unknown error occurred in fetching, creating, or deleting the user.
    """

    def get(self, request, pk=None):
        """
        Handle GET requests to list users or retrieve a specific user.

        Returns:
            APIResponse: A response containing the user data with status code and message.
        Raises:
            LazySettingsException: If there is an exception related to lazy settings.
            Exception: If there is an unknown error occurred in fetching the user.
        """

        try:
            if pk:
                user = get_object_or_404(User, pk=pk)
                serializer = UserDetailSerializer(user)
            else:
                users = User.objects.all()
                serializer = UserDetailSerializer(users, many=True)
            return APIResponse(
                data=serializer.data,
                status_code=status.HTTP_200_OK,
                message="Fetched User Data",
            )
        except settings.LAZY_EXCEPTIONS as ce:
            return APIResponse(
                status_code=ce.status_code,
                errors=ce.error_data(),
                message=ce.message,
                for_error=True,
            )

        except Exception as ce:
            return APIResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                for_error=True,
                message=f"Unknown error occured in fetching user: {ce}",
            )

    def post(self, request):
        """
        Handle POST requests to create a new user.

        Returns:
            APIResponse: A response containing the user data with status code and message.
        Raises:
            LazySettingsException: If there is an exception related to lazy settings.
            Exception: If there is an unknown error occurred in creating the user.
        """

        try:
            serializer = UserCreateSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return APIResponse(
                    data=serializer.data,
                    status_code=status.HTTP_201_CREATED,
                    message="User created Successfully.",
                )
            else:
                return APIResponse(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    for_error=True,
                    message=f"Unknown error occured in creating user: {serializer.errors}",
                )
        except settings.LAZY_EXCEPTIONS as ce:
            return APIResponse(
                status_code=ce.status_code,
                errors=ce.error_data(),
                message=ce.message,
                for_error=True,
            )

        except Exception as ce:
            return APIResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                for_error=True,
                message=f"Unknown error occured in creating user: {ce}",
            )

    def delete(self, request, pk):
        """
        Handle DELETE requests to delete a specific user.

        Returns:
            APIResponse: A response indicating the success or failure of the deletion operation.
        Raises:
            LazySettingsException: If there is an exception related to lazy settings.
            Exception: If there is an unknown error occurred in deleting the user.
        """

        try:
            user = get_object_or_404(User, pk=pk)
            user.delete()
            return APIResponse(
                status_code=status.HTTP_200_OK,
                message=f"User with id : {pk} deleted successfully.",
            )
        except settings.LAZY_EXCEPTIONS as ce:
            return APIResponse(
                status_code=ce.status_code,
                errors=ce.error_data(),
                message=ce.message,
                for_error=True,
            )

        except Exception as ce:
            return APIResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                for_error=True,
                message=f"Unknown error occured in deleting user: {ce}",
            )


class ScheduleAPIView(APIView):
    """
    API view to handle CRUD operations for email schedules.

    This class defines methods to handle GET, POST, and DELETE requests related to email schedules.
    The GET method retrieves a list of email schedules or a specific email schedule.
    The POST method creates a new email schedule.
    The DELETE method deletes a specific email schedule, unless the schedule is already marked as 'Done'.

    Attributes:
        APIView: A class from Django REST framework for creating API views.

    Methods:
        get: Handles GET requests to list email schedules or retrieve a specific email schedule.
        post: Handles POST requests to create a new email schedule.
        delete: Handles DELETE requests to delete a specific email schedule.

    Raises:
        LazySettingsException: If there is an exception related to lazy settings.
        Exception: If there is an unknown error occurred in handling email schedules.
    """

    def get(self, request, pk=None):
        """
        Handle GET requests to list users or retrieve a specific user.

        Returns:
            APIResponse: A response containing the user data with status code and message.

        Raises:
            LazySettingsException: If there is an exception related to lazy settings.
            Exception: If there is an unknown error occurred in fetching the user.
        """
        try:

            if pk:
                schedule = get_object_or_404(EmailSchedule, pk=pk)
                serializer = EmailScheduleDetailSerializer(schedule)
            else:
                query_params = request.query_params
                if query_params:
                    email_status = query_params.get("status")
                    date = query_params.get("date")
                    if email_status and date:
                        query = Q(email_status=email_status) & Q(scheduled_date=date)
                    else:
                        query = Q(email_status=email_status) | Q(scheduled_date=date)
                    schedule = EmailSchedule.objects.filter(query)
                    serializer = EmailScheduleDetailSerializer(schedule, many=True)
                else:
                    schedule = EmailSchedule.objects.all()
                    serializer = EmailScheduleDetailSerializer(schedule, many=True)
            return APIResponse(
                data=serializer.data,
                status_code=status.HTTP_200_OK,
                message="Fetched Email Schedule Data",
            )
        except settings.LAZY_EXCEPTIONS as ce:
            return APIResponse(
                status_code=ce.status_code,
                errors=ce.error_data(),
                message=ce.message,
                for_error=True,
            )

        except Exception as ce:
            return APIResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                for_error=True,
                message=f"Unknown error occured in fetching Email Schedule: {ce}",
            )

    def post(self, request):
        """
        Handle POST requests to create a new user.

        Returns:
            APIResponse: A response containing the user data with status code and message.

        Raises:
            LazySettingsException: If there is an exception related to lazy settings.
            Exception: If there is an unknown error occurred in creating the user.
        """

        try:
            serializer = EmailScheduleCreateSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return APIResponse(
                    data=serializer.data,
                    status_code=status.HTTP_201_CREATED,
                    message="Email Schedule created Successfully.",
                )
            else:
                return APIResponse(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    for_error=True,
                    message=f"Unknown error occured in creating Email Schedule: {serializer.errors}",
                )
        except settings.LAZY_EXCEPTIONS as ce:
            return APIResponse(
                status_code=ce.status_code,
                errors=ce.error_data(),
                message=ce.message,
                for_error=True,
            )

        except Exception as ce:
            return APIResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                for_error=True,
                message=f"Unknown error occured in creating Email Schedule: {ce}",
            )

    def delete(self, request, pk):
        """
        Handle DELETE requests to delete a specific user.

        Returns:
            APIResponse: A response indicating the success or failure of the deletion operation.

        Raises:
            LazySettingsException: If there is an exception related to lazy settings.
            Exception: If there is an unknown error occurred in deleting the user.
        """

        try:
            schedule = get_object_or_404(EmailSchedule, pk=pk)
            if schedule.email_status == "Done":
                return APIResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    for_error=True,
                    message=f"Unknown error occured in creating Email Schedule: Cannot delete schedule that is already done.",
                )
            schedule.delete()
            return APIResponse(
                status_code=status.HTTP_200_OK,
                message=f"Email Schedule with id : {pk} deleted successfully.",
            )
        except settings.LAZY_EXCEPTIONS as ce:
            return APIResponse(
                status_code=ce.status_code,
                errors=ce.error_data(),
                message=ce.message,
                for_error=True,
            )

        except Exception as ce:
            return APIResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                for_error=True,
                message=f"Unknown error occured in deleting Email Schedule: {ce}",
            )


class SendScheduledEmailAPIView(APIView):
    """
    API view to trigger sending scheduled emails based on certain conditions.

    This class defines a method to handle POST requests for triggering the sending of scheduled emails.
    It calculates the current date and time, determines the end time based on the EMAIL_LIMIT setting,
    and filters email schedules that are 'Failed' or 'Pending' and fall within the specified time range.
    For each eligible schedule, it triggers the sending of the email asynchronously.
    The class returns a response indicating the successful triggering of emails.

    Attributes:
        APIView: A class from Django REST framework for creating API views.

    Methods:
        post: Handles POST requests to trigger sending scheduled emails.

    Raises:
        None.
    """

    def post(self, request):
        """
        Handle POST requests to trigger sending scheduled emails.

        This method retrieves the current date and time, calculates the end time based on the EMAIL_LIMIT setting,
        and filters email schedules that are 'Failed' or 'Pending' and fall within the specified time range.
        For each eligible schedule, it triggers the sending of the email asynchronously using a celery task.
        Finally, it returns a response indicating the successful triggering of emails.

        Parameters:
            request (Request): The HTTP POST request object.

        Returns:
            APIResponse: A response indicating the status of the email triggering operation.

        Raises:
            None.
        """

        now = datetime.now()
        current_date = now.date()
        current_time = now.time()

        # EMAIL_LIMIT is a variable used to define the span of time within which emails can be sent.
        # If EMAIL_LIMIT is set to 1 and the endpoint is triggered at 5:00, it will cover all emails sent between 5:00 and 6:00.
        # If EMAIL_LIMIT is set to 2, it will cover emails sent from 5:00 to 7:00.
        email_limit = int(settings.EMAIL_LIMIT)
        email_limit_time = (now + timedelta(hours=email_limit)).time()
        email_schedules = EmailSchedule.objects.filter(
            Q(email_status="Failed") | Q(email_status="Pending"),
            scheduled_date=current_date,
            scheduled_time__gte=current_time,  # Including current time
            scheduled_time__lt=email_limit_time,
        )
        for schedule in email_schedules:
            send_scheduled_email.delay(email_schedule_id=schedule.id)
        return APIResponse(
            status_code=status.HTTP_200_OK,
            message=f"Email(s) Triggered",
        )
