from email.message import EmailMessage

from aiosmtplib import SMTP

from melody.kit.core import config, keyring

__all__ = ("support", "email_message", "send_email_message")

FROM = "From"
TO = "To"
SUBJECT = "Subject"

AUTHOR = "{name} <{email}>"
author = AUTHOR.format


def support() -> str:
    return author(name=config.name, email=config.email.support)


def email_message(author: str, target: str, subject: str, content: str) -> EmailMessage:
    message = EmailMessage()

    message[FROM] = author
    message[TO] = target

    message[SUBJECT] = subject

    message.set_content(content)

    return message


async def send_email_message(message: EmailMessage) -> None:
    email_config = config.email

    client = SMTP(
        hostname=email_config.host,
        port=email_config.port,
        username=keyring.email.username,
        password=keyring.email.password,
        start_tls=True,
    )

    async with client:
        await client.send_message(message)
