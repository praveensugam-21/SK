import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "#f8f9fa",
        sidebar: {
          DEFAULT: "#1e1e2d",
          light: "#1a1a2e"
        },
        primary: {
          DEFAULT: "#3b82f6",
          hover: "#2563eb"
        }
      },
    },
  },
  plugins: [],
};
export default config;
