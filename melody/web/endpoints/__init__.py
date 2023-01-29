from melody.web.endpoints.authentication import get_login, get_register, login, logout, register, verify
from melody.web.endpoints.docs import redirect_docs
from melody.web.endpoints.email import redirect_email
from melody.web.endpoints.github import redirect_github
from melody.web.endpoints.home import get_home
from melody.web.endpoints.keys import get_key
from melody.web.endpoints.redirect import create_redirect

__all__ = (
    # authentication
    "get_login",
    "login",
    "logout",
    "get_register",
    "register",
    "verify",
    # docs
    "redirect_docs",
    # email
    "redirect_email",
    # github
    "redirect_github",
    # home
    "get_home",
    # keys
    "get_key",
    # redirect
    "create_redirect",
)
