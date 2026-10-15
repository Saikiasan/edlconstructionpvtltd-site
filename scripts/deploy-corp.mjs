import { execSync } from 'child_process';
import fs from 'fs';
import path from 'path';

console.log('🚀 Building EDL Corporate Production Bundle...');
execSync('npx astro build', { stdio: 'inherit' });

// Ensure NO root redirect is present in dist/ for corporate domain
const redirectsPath = path.resolve('dist', '_redirects');
if (fs.existsSync(redirectsPath)) {
  fs.unlinkSync(redirectsPath);
  console.log('✓ Cleaned up dist/_redirects for corporate domain');
}

console.log('🌐 Deploying Corporate Platform to edl-construction (Cloudflare Pages)...');
execSync('npx wrangler pages deploy dist --project-name=edl-construction --branch=main', { stdio: 'inherit' });

console.log('✅ Corporate site successfully deployed!');
