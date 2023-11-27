// tailwind.config.js
// Colors from Bulma
module.exports = {
    theme: {
        colors: {
          gray: {
            100: '#f7fafc',
            200: '#edf2f7',
            300: '#e2e8f0',
            400: '#cbd5e0',
            900: '#1a202c',
          },
          red: {
            100: '#fff5f5',
            500: '#f56565',
            600: '#e53e3e',
            700: '#c53030',
            900: '#742a2a',
          },
          green: {
            700: '#2f855a',
          },
          blue: {
            100: '#ebf8ff',
            200: '#bee3f8',
            600: '#3182ce',
            800: '#2c5282',
          },
        },
        screens: {
          sm: '640px',
          md: '768px',
          lg: '1024px',
          xl: '1280px',
        },
        fontFamily: {
          display: ['Gilroy', 'sans-serif'],
          body: ['Cantarell', 'sans-serif'],
        },
        fontSize: {
          xs: '0.75rem',
          sm: '0.875rem',
          base: '1rem',
          lg: '1.125rem',
          xl: '1.25rem',
          '2xl': '1.5rem',
          '3xl': '1.875rem',
          '4xl': '2.25rem',
          '5xl': '3rem',
          '6xl': '4rem',
        },
        borderWidth: {
          DEFAULT: '1px',
          '0': '0',
          '2': '2px',
          '4': '4px',
        },
        extend: {
          colors: {
            primary: '#00d1b2',
            link: '#3273dc',
            info: '#209cee',
            danger: '#ff3860',
            warning: '#ffdd57',
            success: '#23d160',
            'semi-75': 'rgba(0, 0, 0, 0.75)'
          },
          spacing: {
            '96': '24rem',
            '128': '32rem',
          }
        }
    }
  }
