from base64 import urlsafe_b64encode as base64_encode_url_safe
from hashlib import sha256
from secrets import token_urlsafe as token_url_safe

from typing_aliases import Pair

from melody.shared.constants import CODE_VERIFIER_SIZE, DEFAULT_ENCODING, DEFAULT_ERRORS

__all__ = ("PKCE", "generate_pkce")

PKCE = Pair[str]


def generate_pkce(
    size: int = CODE_VERIFIER_SIZE,
    encoding: str = DEFAULT_ENCODING,
    errors: str = DEFAULT_ERRORS,
) -> PKCE:
    verifier = code_verifier(size)
    challenge = code_challenge(verifier, encoding, errors)

    return (verifier, challenge)


def code_verifier(size: int = CODE_VERIFIER_SIZE) -> str:
    return token_url_safe(size)


def code_challenge(
    verifier: str, encoding: str = DEFAULT_ENCODING, errors: str = DEFAULT_ERRORS
) -> str:
    return base64_encode_string(sha256_string(verifier, encoding, errors), encoding, errors)


def sha256_string(
    string: str, encoding: str = DEFAULT_ENCODING, errors: str = DEFAULT_ERRORS
) -> str:
    return sha256(string.encode(encoding, errors)).hexdigest()


BASE64_PADDING = "="


def base64_encode_string(
    string: str,
    encoding: str = DEFAULT_ENCODING,
    errors: str = DEFAULT_ERRORS,
    padding: str = BASE64_PADDING,
) -> str:
    return (
        base64_encode_url_safe(string.encode(encoding, errors))
        .decode(encoding, errors)
        .strip(padding)
    )
