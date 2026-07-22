import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  reactStrictMode: true,
  transpilePackages: ["@vedai/ui", "@vedai/shared"]
};

export default nextConfig;
