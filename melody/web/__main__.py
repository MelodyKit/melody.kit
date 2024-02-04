from entrypoint import entrypoint

from melody.web.main import run

entrypoint(__name__).call(run)
