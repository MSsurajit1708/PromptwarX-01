/** @type {import('next').NextConfig} */
const nextConfig = {
  typescript: {
    ignoreBuildErrors: true,
  },
  eslint: {
    ignoreDuringBuilds: true,
  },
  images: {
    unoptimized: true,
  },
  // Suppress non-standard NODE_ENV warning from Railway/Docker environments
  env: {
    NEXT_TELEMETRY_DISABLED: '1',
  },
}

export default nextConfig
