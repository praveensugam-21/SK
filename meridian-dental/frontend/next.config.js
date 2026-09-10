/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: false,
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://backend:8000/api/:path*',
      },
      {
        source: '/health',
        destination: 'http://backend:8000/health',
      },
    ];
  },
};

module.exports = nextConfig;
