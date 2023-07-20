from melody.web.endpoints.email import redirect_email
from melody.web.endpoints.github import redirect_github
from melody.web.endpoints.index import get_index
from melody.web.endpoints.keys import get_key
from melody.web.endpoints.open import redirect_open
from melody.web.endpoints.redirect import create_redirect

__all__ = (
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
