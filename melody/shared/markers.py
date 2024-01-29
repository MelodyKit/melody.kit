from typing_extensions import Never

__all__ = ("unreachable", "unimplemented")

UNREACHABLE_REACHED = "code path marked as `unreachable` was reached"


def unreachable() -> Never:
    raise RuntimeError(UNREACHABLE_REACHED)


UNIMPLEMENTED = "unimplemented"


def unimplemented() -> Never:
    raise NotImplementedError(UNIMPLEMENTED)
