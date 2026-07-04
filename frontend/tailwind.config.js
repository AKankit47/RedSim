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
                cyber: {
                    950: '#020617',
                    dark: '#0f172a',
                    card: 'rgba(30, 41, 59, 0.8)'
                },
                primary: '#4f46e5'
            }
        },
    },
    plugins: [],
}
