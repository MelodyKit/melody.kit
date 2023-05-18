from melody.web.endpoints.authentication import (
    get_login,
    get_register,
    get_reset,
    login,
    logout,
    register,
    reset,
    revoke,
    verify,
)
from melody.web.endpoints.email import redirect_email
from melody.web.endpoints.github import redirect_github
from melody.web.endpoints.index import get_index
from melody.web.endpoints.keys import get_key
from melody.web.endpoints.open import redirect_open
from melody.web.endpoints.redirect import create_redirect

__all__ = (
    # authentication
    "get_login",
    "login",
    "logout",
    "revoke",
    "get_register",
    "register",
    "verify",
    "get_reset",
    "reset",
    # email
    "redirect_email",
    # github
    "redirect_github",
    # index
    "get_index",
    # keys
    "get_key",
    # open
    "redirect_open",
    # redirect
    "create_redirect",
)
