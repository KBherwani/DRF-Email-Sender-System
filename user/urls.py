"""
This following file in the Django web framework that contains the URL patterns for your web application.
The file maps URLs to views, which are Python functions that handle the incoming HTTP requests
and generate the HTTP response.
"""

from django.urls import path

from .views import ScheduleAPIView, SendScheduledEmailAPIView, UserAPIView

app_name = "user"

urlpatterns = [
    path("api/users/", UserAPIView.as_view(), name="user-create"),
    path("api/users/<int:pk>/", UserAPIView.as_view(), name="user-detail"),
    path("api/schedule/", ScheduleAPIView.as_view(), name="schedule-create"),
    path("api/schedule/<int:pk>/", ScheduleAPIView.as_view(), name="schedule-detail"),
    path(
        "api/email/trigger/", SendScheduledEmailAPIView.as_view(), name="trigger-emails"
    ),
]
