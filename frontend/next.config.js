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

  // ── ESLint ────────────────────────────────────────────────────
  eslint: {
    ignoreDuringBuilds: false,
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

  // ── Experimental Features ─────────────────────────────────────
  experimental: {
    typedRoutes: true,
    instrumentationHook: true,
    serverComponentsExternalPackages: ["bcryptjs", "sharp"],
  },
};

export default nextConfig;
