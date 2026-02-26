/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'asphalt': {
          DEFAULT: '#0D0D0D',
          light: '#1A1A1A',
        },
        'nitrous': '#00D2FF',
        'drs': '#00FF39',
        'championship': '#FF1E23',
        'pit-wall': 'rgba(255, 255, 255, 0.05)',
      },
      fontFamily: {
        'telemetry': ['"Archivo Black"', 'sans-serif'],
        'mono': ['"JetBrains Mono"', 'monospace'],
        'sans': ['Inter', 'system-ui', 'sans-serif'],
      },
      backdropBlur: {
        xs: '2px',
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'slide-in': 'slideIn 0.5s cubic-bezier(0.4, 0, 0.2, 1)',
      },
      keyframes: {
        slideIn: {
          '0%': { transform: 'translateX(-100%)', opacity: '0' },
          '100%': { transform: 'translateX(0)', opacity: '1' },
        },
      },
    },
  },
  plugins: [],
}