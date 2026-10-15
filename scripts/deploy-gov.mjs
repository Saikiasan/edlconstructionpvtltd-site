import { execSync } from 'child_process';
import fs from 'fs';
import path from 'path';

console.log('🚀 Building Government Portal Bundle...');
execSync('npx astro build', { stdio: 'inherit' });

// Add root redirect to /gov for dedicated government subdomain only
const redirectsPath = path.resolve('dist', '_redirects');
fs.writeFileSync(redirectsPath, '/ /gov 200\n', 'utf8');
console.log('✓ Injected root rewrite rule (/ ➔ /gov) into dist/_redirects for gov subdomain');

console.log('🌐 Deploying Government Subdomain to gov-edl-construction (Cloudflare Pages)...');
execSync('npx wrangler pages deploy dist --project-name=gov-edl-construction --branch=main', { stdio: 'inherit' });

// Remove dist/_redirects afterwards so local state is clean
if (fs.existsSync(redirectsPath)) {
  fs.unlinkSync(redirectsPath);
  console.log('✓ Cleaned up temporary dist/_redirects');
}

console.log('✅ Government Subdomain successfully deployed!');
