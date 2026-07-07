import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          DEFAULT: "#C1121F",
          light: "#E23744",
          soft: "#FFF0F0",
        },
        surface: "#F8F8F8",
        ink: "#1C1C1C",
        muted: "#6B7280",
        tip: "#ECFDF5",
        ai: "#E0F2F1",
      },
      fontFamily: {
        sans: ["var(--font-inter)", "system-ui", "sans-serif"],
        display: ["var(--font-poppins)", "system-ui", "sans-serif"],
      },
      boxShadow: {
        card: "0 4px 24px rgba(0,0,0,0.06)",
      },
    },
  },
  plugins: [],
};

export default config;
