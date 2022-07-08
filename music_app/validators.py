from django.core.exceptions import ValidationError


def validate_password(param):
    if len(param) < 8:
        raise ValidationError("Password should be at least 8 characters.")
    elif len(param) > 20:
        raise ValidationError("Password should be no more than 20 characters.")
    elif not any(char.isdigit() for char in param):
        raise ValidationError("Password should have at least one number.")
