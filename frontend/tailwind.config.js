/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'green': {
          600: '#3da37a',
          700: '#62c2a0'
        }
      }
    },
  },
  plugins: [],
}