from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.conf import settings

from user.models import User
from base.utils.jwt_decoder import decode_jwt


@database_sync_to_async
def get_user(jwt):
    try:
        user_id = decode_jwt(jwt)
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return AnonymousUser()


class JWTAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        headers = dict(scope["headers"])
        if b"authorization" in headers:
            try:
                token = headers[b"authorization"].decode().split()[1]
                scope["user"] = await get_user(token)
            except IndexError:
                pass
        return await super().__call__(scope, receive, send)
