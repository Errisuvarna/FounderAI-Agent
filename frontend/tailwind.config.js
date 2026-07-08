/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        ink: {
          950: '#080D18',
          900: '#0B1220',
          800: '#12192B',
          700: '#182238',
          600: '#24314C',
          500: '#3A4A6B',
        },
        paper: {
          100: '#E8ECF4',
          300: '#B7C1D6',
          500: '#8A96AC',
        },
        blueprint: {
          400: '#8FF5E4',
          500: '#5EEAD4',
          600: '#2BC4AC',
        },
        stamp: {
          400: '#F7B94D',
          500: '#F5A623',
          600: '#D98C10',
        },
        danger: {
          500: '#F26D6D',
        },
      },
      fontFamily: {
        display: ['"Space Grotesk"', 'sans-serif'],
        body: ['"Inter"', 'sans-serif'],
        mono: ['"JetBrains Mono"', 'monospace'],
      },
      backgroundImage: {
        'blueprint-grid':
          'linear-gradient(rgba(94,234,212,0.06) 1px, transparent 1px), linear-gradient(90deg, rgba(94,234,212,0.06) 1px, transparent 1px)',
      },
      backgroundSize: {
        grid: '28px 28px',
      },
      boxShadow: {
        panel: '0 0 0 1px rgba(94,234,212,0.08), 0 20px 60px -20px rgba(0,0,0,0.6)',
      },
      keyframes: {
        draw: {
          '0%': { strokeDashoffset: '1' },
          '100%': { strokeDashoffset: '0' },
        },
        pulseDot: {
          '0%, 100%': { opacity: 0.4 },
          '50%': { opacity: 1 },
        },
      },
      animation: {
        pulseDot: 'pulseDot 1.4s ease-in-out infinite',
      },
    },
  },
  plugins: [],
}
