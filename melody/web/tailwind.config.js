const defaultTheme = require("tailwindcss/defaultTheme");

module.exports = {
    content: ["./**/*.html"],
    darkMode: "media",
    theme: {
        extend: {
            colors: {
                // melody
                "melody-purple": "#cc55ff",
                "melody-blue": "#55ccff",
                // brands
                discord: "#5865f2",
                youtube: "#ff0000",
                twitter: "#1da1f2",
                reddit: "#ff5700",
            },
            fontFamily: {
                sans: ["Gotham Pro", ...defaultTheme.fontFamily.sans]
            }
        }
    }
}
