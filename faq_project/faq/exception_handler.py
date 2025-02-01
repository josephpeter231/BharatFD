# faq/exception_handler.py
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.urls import reverse

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    # If the exception is a 404, redirect to the FAQ list view
    if response is not None and response.status_code == status.HTTP_404_NOT_FOUND:
        faq_url = reverse('faq-list') + '?lang=en'
        return Response(status=status.HTTP_302_FOUND, headers={"Location": faq_url})

    return response