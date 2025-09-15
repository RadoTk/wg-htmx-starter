/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './rootapp/templates/**/*.html',
    './rootapp/templates/**/*.js',
    './rootapp/static/js/**/*.js',
  ],
  theme: {
    extend: {
      // Personnalisations du thème ici
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
  ],
}