# properties/validators.py
from django.core.exceptions import ValidationError
import re

def validate_file_size(value):
    filesize= value.size
    if filesize > 10248576:
        raise ValidationError("The maximum file size that can be uploaded is 10MB")
    else:
        return value

def validate_postcode(value):
    if re.match("^[a-zA-Z0-9 ]*$", value):
        return value
    else:
        raise ValidationError('Please use a valid postal code format')