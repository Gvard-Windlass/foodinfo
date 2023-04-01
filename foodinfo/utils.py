from __future__ import unicode_literals
from django.db import IntegrityError
from rest_framework.views import Response, exception_handler
from rest_framework import status
from rest_framework import serializers


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first to get the standard error response.
    response = exception_handler(exc, context)

    # if there is an IntegrityError and the error response hasn't already been generated
    if isinstance(exc, IntegrityError) and not response:
        response = Response(
            {
                "message": "It seems there is a conflict between the data you are trying to save and your current "
                "data. Please review your entries and try again."
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    return response


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional 'fields' argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop("fields", None)

        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the 'fields' argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)
