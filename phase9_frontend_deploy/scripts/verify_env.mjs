/**
 * Fail Vercel builds when NEXT_PUBLIC_API_URL is missing.
 * Skips locally unless VERCEL=1 is set.
 */

const isVercel = process.env.VERCEL === "1";
const apiUrl = process.env.NEXT_PUBLIC_API_URL?.trim();

if (isVercel && !apiUrl) {
  console.error(
    "NEXT_PUBLIC_API_URL is required on Vercel. Set it to your Render API URL (e.g. https://bitewise-api.onrender.com).",
  );
  process.exit(1);
}

if (apiUrl?.endsWith("/")) {
  console.warn(
    "NEXT_PUBLIC_API_URL should not end with a trailing slash; the client strips it automatically.",
  );
}

console.log(
  isVercel
    ? `Vercel build: API URL -> ${apiUrl}`
    : "Local build: using NEXT_PUBLIC_API_URL or http://127.0.0.1:8000 default",
);
