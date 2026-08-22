/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        bg: {
          primary: '#0A0A0B',
          secondary: '#111114',
          card: 'rgba(26, 26, 32, 0.65)',
          'card-hover': 'rgba(38, 38, 48, 0.85)',
          glass: 'rgba(255, 255, 255, 0.03)',
        },
        navy: {
          900: '#0D2560',
          800: '#1c4294',
          700: '#244c9d',
          600: '#2d56a7',
          500: '#345eae',
        },
        gold: {
          primary: '#C9A84C',
          light: '#D4B96A',
          dark: '#A07830',
          subtle: 'rgba(201, 168, 76, 0.15)',
        },
        accent: {
          orange: '#EF3800',
          cyan: '#00f2ff',
          green: '#22c55e',
          red: '#ef4444',
          yellow: '#f59e0b',
        },
        border: {
          subtle: 'rgba(255, 255, 255, 0.08)',
          glow: 'rgba(201, 168, 76, 0.35)',
          cyan: 'rgba(0, 242, 255, 0.35)',
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        heading: ['Outfit', 'sans-serif'],
        mono: ['JetBrains Mono', 'Fira Code', 'monospace'],
      },
      boxShadow: {
        glass: '0 8px 32px 0 rgba(0, 0, 0, 0.45)',
        gold: '0 0 25px rgba(201, 168, 76, 0.25)',
        cyan: '0 0 25px rgba(0, 242, 255, 0.25)',
        card: '0 4px 24px rgba(0, 0, 0, 0.5)',
      },
      backdropBlur: {
        xs: '2px',
      }
    },
  },
  plugins: [],
}
