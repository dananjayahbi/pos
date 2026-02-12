/** @type {import('next').NextConfig} */
const nextConfig = {
  // ── Basic Settings ────────────────────────────────────────────
  reactStrictMode: true,
  poweredByHeader: false,
  output: "standalone",

  // ── TypeScript ────────────────────────────────────────────────
  typescript: {
    ignoreBuildErrors: false,
  },

  // ── Images ────────────────────────────────────────────────────
  images: {
    formats: ["image/avif", "image/webp"],
    remotePatterns: [
      {
        protocol: "http",
        hostname: "localhost",
        port: "",
        pathname: "/**",
      },
      {
        protocol: "https",
        hostname: "*.lankacommerce.lk",
        port: "",
        pathname: "/images/**",
      },
      {
        protocol: "https",
        hostname: "cdn.lankacommerce.lk",
        port: "",
        pathname: "/**",
      },
      {
        protocol: "https",
        hostname: "storage.googleapis.com",
        port: "",
        pathname: "/**",
      },
      {
        protocol: "https",
        hostname: "res.cloudinary.com",
        port: "",
        pathname: "/**",
      },
    ],
  },

  // ── Server External Packages (moved from experimental) ───────
  serverExternalPackages: ["bcryptjs", "sharp"],

  // ── Typed Routes (moved from experimental) ────────────────────
  typedRoutes: true,
};

export default nextConfig;
