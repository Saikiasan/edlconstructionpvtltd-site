/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        gold: { 400: '#D4AF37', 500: '#C5A059', 600: '#A6823F' },
        primary: {
          DEFAULT: '#0F172A', // Structural Navy
          navy: '#0F172A',
          hover: '#1E293B'
        },
        secondary: {
          DEFAULT: '#0369A1', // Blueprint Teal
          teal: '#0369A1',
          hover: '#0284C7',
          light: '#E0F2FE'
        },
        accent: {
          DEFAULT: '#EA580C', // Safety Orange
          orange: '#EA580C',
          hover: '#C2410C',
          light: '#FFEDD5'
        },
        neutralSurface: {
          DEFAULT: '#F1F5F9', // Light Platinum
          platinum: '#F1F5F9'
        },
        textDark: {
          DEFAULT: '#020617', // Iron Black
          iron: '#020617'
        }
      },
      fontFamily: {
        sans: ['Plus Jakarta Sans', 'sans-serif'],
        serif: ['Playfair Display', 'serif'],
        syne: ['Syne', 'sans-serif']
      }
    }
  },
  plugins: []
};
