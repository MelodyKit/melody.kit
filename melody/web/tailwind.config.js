const defaultTheme = require("tailwindcss/defaultTheme");

module.exports = {
    content: ["./templates/**/*.html"],
    darkMode: "media",
    theme: {
        extend: {
            colors: {
                // melody
                "melody-purple": "#cc55ff",
                "melody-blue": "#55ccff",
                // errors
                error: "#ff0000",
                // brands
                discord: "#5865f2",
                youtube: "#ff0000",
                twitter: "#1da1f2",
                reddit: "#ff5700",
                telegram: "#229ed9",
            },
            fontFamily: {
                sans: ["Gotham Pro", ...defaultTheme.fontFamily.sans]
            },
        }
    },
};
