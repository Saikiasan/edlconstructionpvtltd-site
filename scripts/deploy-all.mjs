import { execSync } from 'child_process';

console.log('=== 1/2 Deploying Corporate Main Platform ===');
execSync('node scripts/deploy-corp.mjs', { stdio: 'inherit' });

console.log('\n=== 2/2 Deploying Dedicated Government Subdomain ===');
execSync('node scripts/deploy-gov.mjs', { stdio: 'inherit' });

console.log('\n🎉 All deployments completed successfully!');
