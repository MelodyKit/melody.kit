from typing_aliases import StringDict

__all__ = (
    "USER_FOLLOWING_READ",
    "USER_FOLLOWING_WRITE",
    "USER_LIBRARY_READ",
    "USER_LIBRARY_WRITE",
    "USER_PLAYLISTS_READ",
    "USER_PLAYLISTS_WRITE",
    "USER_SETTINGS_READ",
    "USER_SETTINGS_WRITE",
    "USER_IMAGE_READ",
    "USER_IMAGE_WRITE",
    "USER_STREAMS_READ",
    "USER_STREAMS_WRITE",
    "SCOPE_SETUP",
    "ScopeSetup",
)

USER_FOLLOWING_READ = "user-following-read"
USER_FOLLOWING_WRITE = "user-following-write"
USER_LIBRARY_READ = "user-library-read"
USER_LIBRARY_WRITE = "user-library-write"
USER_PLAYLISTS_READ = "user-playlists-read"
USER_PLAYLISTS_WRITE = "user-playlists-write"
USER_SETTINGS_READ = "user-settings-read"
USER_SETTINGS_WRITE = "user-settings-write"
USER_IMAGE_READ = "user-image-read"
USER_IMAGE_WRITE = "user-image-write"
USER_STREAMS_READ = "user-streams-read"
USER_STREAMS_WRITE = "user-streams-write"

ScopeSetup = StringDict[str]  # scope -> description

SCOPE_SETUP = {
    USER_FOLLOWING_READ: "Read access to the user's following.",
    USER_FOLLOWING_WRITE: "Write access to the user's following.",
    USER_LIBRARY_READ: "Read access to the user's library.",
    USER_LIBRARY_WRITE: "Write access to the user's library.",
    USER_PLAYLISTS_READ: "Read access to the user's playlists.",
    USER_PLAYLISTS_WRITE: "Write access to the user's playlists.",
    USER_SETTINGS_READ: "Read access to the user's settings.",
    USER_SETTINGS_WRITE: "Write access to the user's settings.",
    USER_IMAGE_READ: "Read access to the user's image.",
    USER_IMAGE_WRITE: "Write access to the user's image.",
    USER_STREAMS_READ: "Read access to the user's streams.",
    USER_STREAMS_WRITE: "Write access to the user's streams.",
}
