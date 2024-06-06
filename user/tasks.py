from datetime import datetime
from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.http import BadHeaderError
from django.db.models import Q


from .models import EmailSchedule

@shared_task
def send_scheduled_email(email_schedule_id):
    """
    Function to send a scheduled email.

    Parameters:
    email_schedule_id (int): The ID of the email schedule to be processed.

    Returns:
    str: A message indicating the result of the email sending process.

    Raises:
    Exception: If an error occurs during the email sending process.
    """
    
    schedule = EmailSchedule.objects.get(id = email_schedule_id)
    try:
        email_response = email_handler(schedule.user.email)
        if email_response.get("status"):
            schedule.email_status = "Done"
            return "Email sent sucessfully."
        else:
            schedule.email_status = "Failed"
            return "Email sent failed."
    except Exception as e:
        schedule.email_status = "Failed"
        import traceback
        return "Unkown error occured while sending email:" + str(e) + str(traceback.print_exc())
    
    finally:
        schedule.save()

@shared_task
def resend_email():
    """
    Function to resend emails for failed or pending email schedules.

    Returns:
        str: A message indicating the result of the email resending process.

    Raises:
        Exception: If an error occurs during the email resending process.
    """
    
    try:
        now = datetime.now()
        current_date = now.date()
        schedule = None
        email_schedules = EmailSchedule.objects.filter(
            Q(email_status='Failed') |  # Condition 1: Records where status is 'Failed'
            (Q(scheduled_date__lt=current_date) & (Q(email_status='Failed') | Q(email_status='Pending')))  # Condition 2: Records where date is in past and status is 'Failed' or 'Pending'
        )
        for schedule in email_schedules:
            email_response = email_handler(schedule.user.email)
            if email_response.get("status"):
                schedule.email_status = "Done"
                return "Email sent sucessfully."
            else:
                schedule.email_status = "Failed"
                return "Email sent failed."
    except Exception as e:
       return "Failed to resend email:" + str(e)
    finally:
       if schedule:
        schedule.save()
   
def email_handler(email):
    """
    Function to handle sending email using Django's send_mail function.

    Parameters:
    email (str): The email address of the recipient.

    Returns:
    dict: A dictionary containing the status of the email sending process.
        - status (bool): True if the email was sent successfully, False otherwise.
        - message (str): A message indicating the result of the email sending process.

    Raises:
    BadHeaderError: If there is an issue with the email headers.
    Exception: If any other exception occurs during the email sending process.
    """
    try:
        host_email = settings.EMAIL_HOST_USER
        user_email = email
        mail_subject = 'Email Sender System'
        mail_content = 'This is a mail send from Email Sender System'
        send_mail(
            subject=mail_subject,
            message=mail_content,
            from_email=host_email,
            recipient_list=[user_email],
            fail_silently=False,
        )
        return {"status":True,
                "message":"Email sent sucessfully"
                }
    except BadHeaderError:
        return {"status":False,
                "message":"Error while sending email"
                }
    except Exception as e:
        return {"status":False,
                "message":"Error while sending email"
        }
