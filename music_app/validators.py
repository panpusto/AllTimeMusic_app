from django.core.exceptions import ValidationError


def validate_password(param):
    special_symbols = ['!', '@', '#', '%']

    if len(param) < 8:
        raise ValidationError("Password should be at least 8 characters.")
    elif len(param) > 20:
        raise ValidationError("Password should be no more than 20 characters.")
    elif not any(char.isdigit() for char in param):
        raise ValidationError("Password should have at least one number.")
    elif not any(char.islower() for char in param):
        raise ValidationError("Password should have at least one lower case letter.")
    elif not any(char in special_symbols for char in param):
        raise ValidationError("Password should have at least on of these symbols: !, @, #, %.")
