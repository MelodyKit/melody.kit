insert Artist {
    name := "pyrokinesis",
    genres := ["Rap"],
    spotify_id := "5rXtHvb8jMNgmSX7Khd77x",
    apple_music_id := "1106141235",
    yandex_music_id := "5313769",
};

insert Track {
    artists := (select Artist filter .name = "pyrokinesis"),
    explicit := false,
    duration_ms := 160000,
    name := "молот ведьм (Remastered 2023)",
    spotify_id := "08INrFjE7BNPN4WqxPOmUC",
    apple_music_id := "1668210318",
    yandex_music_id := "111008969",
};

insert Album {
    artists := (select Artist filter .name = "pyrokinesis"),
    tracks := (select Track { @position := 0 } filter .name = "молот ведьм (Remastered 2023)"),
    album_type := AlbumType.`single`,
    release_date := <cal::local_date>"2023-02-10",
    label := "Rhymes Music",
    genres := ["Rap"],
    name := "молот ведьм (Remastered 2023)",
    spotify_id := "4Vf8K74oVZV6IyUOgyV4MZ",
    apple_music_id := "1668210316",
    yandex_music_id := "24743055",
};
