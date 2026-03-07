const fs = require('fs');

async function checkAndRemind() {
  const planPath = 'memory/projects/project-seed/specs/product-plan.md';
  if (!fs.existsSync(planPath)) return;

  const content = fs.readFileSync(planPath, 'utf8');
  const allDone = !content.includes('[ ]'); // Check if any unchecked boxes remain

  if (allDone) {
    console.log('AGENT_GUNNA_UPDATE: All milestones for Project Seed are complete! Ready for launch review.');
  } else {
    // Log progress for heartbeat visibility
    const total = (content.match(/\[[ x]\]/g) || []).length;
    const done = (content.match(/\[x\]/g) || []).length;
    console.log(`AGENT_GUNNA_PROGRESS: Project Seed is ${done}/${total} milestones complete.`);
  }
}

checkAndRemind();
