"""
The following file is part of the Django web framework and contains the views for your web application.
The file defines view functions or classes that handle the incoming HTTP requests and generate the HTTP responses.
Each view encapsulates the logic for processing requests, such as retrieving data from the database,
performing calculations, and rendering templates or returning data in various formats (e.g., JSON, HTML).
"""

from django.shortcuts import render
from django.views import View

class IndexView(View):
    """
    View for Main Landing Page
    """

    template_name = "index.html"

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name)