"""
defines how models are displayed and managed in the Django admin interface. It allows customization of admin site behavior, 
such as registering models, specifying display fields, and configuring filters
"""

from django.contrib import admin

from user.models import EmailSchedule, User

admin.site.register(User)
admin.site.register(EmailSchedule)