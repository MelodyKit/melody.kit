module default {
    type Playlist extending Base {
        multi link tracks -> Track;
    }
}