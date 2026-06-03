/** @type {import('next').NextConfig} */
const nextConfig = {
  // Allow reading YAML from sibling data/ folder at build time
  outputFileTracingIncludes: {
    '/**/*': ['./data/**/*'],
  },
};

export default nextConfig;
