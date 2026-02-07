import os
from typing import Optional, Dict, Any
from fastapi import Request
from pydantic import BaseModel
from fastapi_azure_auth import SingleTenantAzureAuthorizationCodeBearer

from .env import APP_CLIENT_ID, TENANT_ID

class DummyUser(BaseModel):
    preferred_username: str
    name: str = "Dummy User"
    roles: list[str] = []
    aud: str = "dummy"
    tid: str = "dummy"
    oid: str = "dummy"
    sub: str = "dummy"
    ver: str = "2.0"
    claims: Dict[str, Any] = {}

class DummyOpenIDConfig:
    async def load_config(self):
        pass

class DummyScheme:
    def __init__(self):
        self.openid_config = DummyOpenIDConfig()
        
    async def __call__(self, request: Request):
        # Allow switching users via header for testing
        username = request.headers.get("x-dummy-user", "admin@example.com")
        return DummyUser(preferred_username=username)

if os.environ.get("AUTH_MODE") == "dummy":
    azure_scheme = DummyScheme()
else:
    azure_scheme = SingleTenantAzureAuthorizationCodeBearer(
        app_client_id=APP_CLIENT_ID,
        tenant_id=TENANT_ID,
        scopes={
            # Key is the scope name, value is the description.
            f"api://{APP_CLIENT_ID}/user_impersonation": "User impersonation",
            "User.Read": "Read user profile",
            "Mail.Send": "Send mail as user",
        },
    )

swagger_scheme = {
    "swagger_ui_oauth2_redirect_url": "/",
    "swagger_ui_init_oauth": {
        "usePkceWithAuthorizationCodeGrant": True,
        "clientId": APP_CLIENT_ID,
    },
}
