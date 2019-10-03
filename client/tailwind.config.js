// tailwind.config.js
// Colors from Bulma
module.exports = {
    theme: {
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
        borderWidth: {
          default: '1px',
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