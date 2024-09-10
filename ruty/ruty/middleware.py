from urllib.parse import parse_qs
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from rest_framework.authtoken.models import Token

@database_sync_to_async
def get_user(token_key):
    try:
        token = Token.objects.get(key=token_key)
        return token.user
    except Token.DoesNotExist:
        return AnonymousUser()

class TokenAuthMiddleWare:

    def __init__(self, inner):
        self.inner = inner
    def __call__(self, scope):
        return TokenAuthMiddleWareInstance(scope, self.inner)

class TokenAuthMiddleWareInstance:
    def __init__(self, scope, inner):
        self.scope = scope
        self.inner = inner

        async def __call__(self, receive, send):
            query_string = self.scope['query_string'].decode()
            params = parse_qs(query_string)
            token_key = params.get('token')
            if token_key:
                token_key = token_key[0]
                user = await get_user(token_key)
                self.scope['user'] = user
            else:
                self.scope['user'] = AnonymousUser()
            return await self.inner(self.scope)(receive, send)