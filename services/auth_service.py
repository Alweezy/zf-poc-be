import os
import requests
from urllib.parse import urlencode
from dotenv import load_dotenv

load_dotenv()

AUTH_DOMAIN = os.getenv("AUTH_DOMAIN")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

# Temporary token store (in-memory, for demo)
_tokens = {}


def build_authorization_url():
    """Generate the URL to redirect the user to Auth0 for login."""
    params = {
        "response_type": "code",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": "openid profile email offline_access",
        "audience": "https://api.prod.zaehlerfreunde.com",
    }
    return f"{AUTH_DOMAIN}/authorize?{urlencode(params)}"


def exchange_code_for_token(code):
    """Exchange authorization code for access + refresh tokens."""
    token_url = f"{AUTH_DOMAIN}/oauth/token"
    payload = {
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": code,
        "redirect_uri": REDIRECT_URI,
    }

    response = requests.post(token_url, json=payload)
    response.raise_for_status()
    tokens = response.json()

    _tokens["access_token"] = tokens.get("access_token")
    _tokens["refresh_token"] = tokens.get("refresh_token")

    return tokens


def get_access_token():
    """Return a valid access token (refresh if needed)."""
    token = _tokens.get("access_token")
    if token:
        return token

    raise RuntimeError("No access token found — user must authenticate first.")


def refresh_access_token():
    """Use refresh_token to get a new access_token."""
    if "refresh_token" not in _tokens:
        raise RuntimeError("No refresh token available to renew access.")

    token_url = f"{AUTH_DOMAIN}/oauth/token"
    payload = {
        "grant_type": "refresh_token",
        "client_id": CLIENT_ID,
        "refresh_token": _tokens["refresh_token"],
    }

    response = requests.post(token_url, json=payload)
    response.raise_for_status()
    new_data = response.json()

    _tokens["access_token"] = new_data.get("access_token")
    return _tokens["access_token"]