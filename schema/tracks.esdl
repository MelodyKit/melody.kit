module default {
    type Track extending Base {
        required multi link artists -> Artist;
    }
}
