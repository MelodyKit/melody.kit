from entrypoint import entrypoint

from melody.web.main import web

entrypoint(__name__).call(web)
