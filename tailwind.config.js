/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/templates/**/*.html",
    "./app/static/**/*.js",
    "./app/blog/templates/**/*.html"  // Add this line
  ],
  theme: {
    extend: {},
  },
  fontFamily: {
    sans: ['Inter', 'ui-sans-serif', 'system-ui', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'Helvetica Neue', 'Arial', 'sans-serif'],
    serif: ['Georgia', 'serif'],
  },
  colors: {
    blue: {
      50: '#e8eaf6',
      100: '#c5cae9',
      500: '#3949ab',
      600: '#283593',
      700: '#1a237e',
    },
    green: {
      500: '#2e7d32',
    }
  },
  plugins: [
    require('@tailwindcss/typography'),
  ],
}