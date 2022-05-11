/** @type {import('next').NextConfig} */
const nextConfig = {
    reactStrictMode: false,
    images: {
        domains: ['localhost', 'localhost:3000', 's1.ax1x.com'],
    },
    experimental: {
        outputStandalone: true,
    },
}

module.exports = nextConfig
