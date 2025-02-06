/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    // Include all Django HTML and template files
    "./templates/**/*.html", // Templates at the project level
    "./**/templates/**/*.html", // Templates inside apps
    "./static/**/*.js", // JavaScript files in the static folder
    "./**/static/**/*.js", // JavaScript files in app-level static folders
    "./**/templatetags/**/*.py",
  ],
  theme: {
    extend: {
      // Customizations for your design
      colors: {
        primary: "#1d4ed8", // Example custom color
        secondary: "#9333ea",
      },
      fontFamily: {
        sans: ["Inter", "sans-serif"], // Example custom font
      },
    },
  },
  plugins: [],
};
