import { spawn } from "node:child_process";

import {
  cleanupBuildOutputs,
  repositoryRoot,
} from "./cleanup-build-output.mjs";

function run(command, args) {
  return new Promise((resolve, reject) => {
    const child = spawn(command, args, {
      cwd: repositoryRoot,
      stdio: "inherit",
      shell: false,
    });

    child.once("error", reject);
    child.once("exit", (code, signal) => {
      if (code === 0) {
        resolve();
        return;
      }

      const reason = signal ? `signal ${signal}` : `exit code ${code}`;
      reject(new Error(`${command} failed with ${reason}`));
    });
  });
}

async function main() {
  await cleanupBuildOutputs();
  try {
    await run("zola", ["build"]);
  } finally {
    await cleanupBuildOutputs();
  }
}

main().catch((error) => {
  console.error(`[build] ${error.message}`);
  process.exitCode = 1;
});
