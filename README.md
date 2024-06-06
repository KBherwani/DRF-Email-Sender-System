# Email Sender System
This is a simple yet robust system for sending scheduled emails to users based on their specified time preferences. It includes modules for managing user details, scheduling emails, and sending emails asynchronously via an API call. The backend utilizes Celery for task queuing and Redis as a message broker for efficient asynchronous processing.

# User Module
This module manages user details and ensures the presence of an email column, which is essential for the functioning of the entire system.

# Functionalities
Create / Delete User: Allows the creation and deletion of user profiles, ensuring the presence of necessary information including email addresses.
List Users: Provides functionality to list all existing users along with their details.
Scheduled Emails
This module handles the scheduling of emails for users, allowing them to specify preferred times to receive emails. Users can have multiple entries in the scheduling table to receive emails at different times.

# Functionalities
Create / Delete Schedule: Enables users to create or delete scheduled entries for receiving emails at specific times.
List Schedules: Provides a list of all scheduled email entries for users.
Send Emails
This is the core functionality of the system, responsible for sending emails to users based on their scheduled times. It utilizes an API to trigger email sending, ensuring asynchronous processing for efficiency.

# Functionalities
Asynchronous Email Sending: Emails are sent in the background asynchronously, triggered by calling the designated API endpoint.
Live Status Updates: Implements live status updates to monitor the progress of email sending, displaying the number of emails sent and pending.
Retry Functionality: Utilizes Celery's retry mechanism to handle errors during email sending, automatically retrying failed tasks for seamless operation.

# Implementation Details
Backend: Choose your preferred backend for storing user data and scheduling information.
Celery and Redis: Utilizes Celery for task queuing and Redis as the message broker for efficient background task processing.
API Integration: Integrates with an API to trigger email sending based on scheduled times.
Usage

# Prerequisites
Python 3.x installed on your system
Pipenv installed (pip install pipenv)
Redis server installed and running
Steps to Run
Clone the Repository:

git clone <repository_url>
Navigate to Project Directory:

cd <project_directory>
Install Dependencies:

pipenv install
Activate Virtual Environment:

pipenv shell
Run Django Migrations:

python manage.py migrate
Start Celery Worker:

css
celery -A <project_name> worker --loglevel=info
Start Celery Beat (for scheduled tasks):

css
celery -A <project_name> beat -l info

Run Django Development Server:
python manage.py runserver

Access the Application:
Visit http://localhost:8000 in your web browser to access the application.

# Note:
Replace <repository_url> with the URL of your Git repository.
Replace <project_directory> with the directory where you cloned the repository.
Replace <project_name> with the name of your Django project.

These steps assume you have a basic understanding of Django development. Make sure to configure your Django project settings, such as database settings, API endpoints, and email configurations, according to your requirements before running the system.

# Contributing
Contributions to enhance the system with additional features or improvements are welcome. Please fork the repository, make your changes, and submit a pull request for review.

# License
This project is licensed under the MIT License. Feel free to modify and distribute it for your own purposes.

