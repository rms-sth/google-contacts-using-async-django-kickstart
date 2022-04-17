import asyncio
import json

from aiogoogle.auth.creds import (  # noqa: E402 module level import not at top of file
    ClientCreds,
    UserCreds,
)
from allauth.socialaccount.models import SocialToken
from asgiref.sync import async_to_sync, sync_to_async
from django.conf import settings
from django.http import HttpResponse
from django.utils.decorators import classonlymethod
from django.views.generic import View

from login.utils import list_contacts


def get_user_cred(access_token, refresh_token, expires_at=None):
    user_creds = UserCreds(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_at=expires_at,
    )
    return user_creds


def get_client_cred(client_id, client_secret, scopes: list):
    client_creds = ClientCreds(
        client_id=client_id,
        client_secret=client_secret,
        scopes=scopes,
    )
    return client_creds


@sync_to_async
def _get_social_token(user):
    token = (
        SocialToken.objects.filter(account__user=user)
        .select_related("app", "account")
        .first()
    )
    return token


class BaseAsyncView(View):
    """Base Async View."""

    @classonlymethod
    def as_view(cls, **initkwargs):
        view = super().as_view(**initkwargs)
        view._is_coroutine = asyncio.coroutines._is_coroutine
        return view


class ContactList(BaseAsyncView):
    async def get(self, request):
        token = await _get_social_token(request.user)
        if token:
            user_creds = get_user_cred(
                access_token=token.token,
                refresh_token=token.token_secret,
            )
            client_creds = get_client_cred(
                client_id=token.app.client_id,
                client_secret=token.app.secret,
                scopes=settings.SCOPES,
            )
            contacts = await list_contacts(
                user_creds=user_creds, client_creds=client_creds
            )
            return HttpResponse(
                json.dumps(contacts, indent=2),
                content_type="application/json; charset=utf8",
            )
