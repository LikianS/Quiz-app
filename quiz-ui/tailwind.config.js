/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        'custom-dark': 'rgb(37, 39, 41)',
        'main-violet': '#C4AFF0',
      },
      keyframes: {
        zoomSlow: {
          '0%, 100%': { transform: 'scale(1)' },
          '50%': { transform: 'scale(1.05)' },
        },
      },
      animation: {
        'zoom-slow': 'zoomSlow 10s ease-in-out infinite',
      },
    },
  },
  plugins: [],
};
