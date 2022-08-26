module default {
    type Base {
        required property name -> str;

        required property image -> str;

        required property created_at -> datetime {
            default := datetime_current();
            readonly := true;
        };

        property spotify_id -> str;
        property apple_music_id -> str;
        property yandex_music_id -> str;
    }
}
