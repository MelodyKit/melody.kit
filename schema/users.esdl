module default {
    type User extending Base {
        required property email -> str {
            constraint exclusive;
        };
        required property password -> str;
    }
}
