use melody_enum::melody_enum;

melody_enum! {
    #[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Default)]
    pub Type {
        #[default]
        Album => album,
        Single => single,
        Compilation => compilation,
    }
}
