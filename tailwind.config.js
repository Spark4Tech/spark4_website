/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/templates/**/*.html",
    "./app/static/**/*.js",
    "./app/blog/templates/**/*.html"
  ],
  theme: {
    extend: {
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
    }
  },
  plugins: [
    require('@tailwindcss/typography'),
    // Add a plugin to inject the custom styles for HTMX service details
    function({ addComponents }) {
      const components = {
        '.service-card': {
          height: '450px',
          position: 'relative',
        },
        '.service-details': {
          position: 'absolute',
          left: '0',
          right: '0',
          top: '100%',
          marginTop: '0',
          backgroundColor: 'rgb(31 41 55)',
          borderRadius: '0 0 0.75rem 0.75rem',
          zIndex: '10',
          borderTop: '1px solid rgb(55 65 81)',
          boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
          opacity: '0',
          maxHeight: '0',
          overflow: 'hidden',
          transition: 'opacity 0.3s ease, max-height 0.5s ease',
          '&:not(.hidden)': {
            opacity: '1',
            maxHeight: '1000px',
          },
        },
        // other custom components...
      }
      addComponents(components)
    }
  ],
}