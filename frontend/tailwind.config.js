/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        custom: {
          teal: '#269588',
        },
        'primary': {
          DEFAULT: '#3da37a',
          'light': '#62c2a0',
          'dark': '#2c7758',
        },
        'bg': {
          DEFAULT: '#e6eef5',
          'card': '#ffffff',
        },
        'memory': {
          DEFAULT: '#c3d7f5',
        },
        'text': {
          'primary': '#333333',
          'secondary': '#666666',
        },
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },
      borderRadius: {
        'card': '10px',
      },
      boxShadow: {
        'card': '0 4px 6px rgba(0, 0, 0, 0.05)',
      }
    },
  },
  plugins: [],
}