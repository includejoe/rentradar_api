from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import jwt as JWT
import environ

env = environ.Env()
environ.Env.read_env()


def decode_jwt(token):
    # slicing the authorization header to get jwt without "Bearer "
    jwt = token[7:]
    payload = JWT.decode(jwt, env("JWT_SECRET_KEY"), env("JWT_ALGORITHM"))
    return payload["user_id"]


def is_email_valid(value):
    # Validate a single email
    message_invalid = "Enter a valid email address"

    if not value:
        return False, message_invalid

    # Check the regex, using the validate_email from django
    try:
        validate_email(value)
    except ValidationError:
        return False, message_invalid

    return True, ""


def action_response(success, info):
    return {
        "success": success,
        "info": info,
    }
