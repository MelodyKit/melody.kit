use melody_enum::melody_enum;

melody_enum! {
    #[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
    pub Type {
        Track => track,
        Artist => artist,
        Album => album,
        Playlist => playlist,
        User => user,
    }
}
