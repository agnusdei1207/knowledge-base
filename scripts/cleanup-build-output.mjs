import { readdir, rm } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const scriptDirectory = path.dirname(fileURLToPath(import.meta.url));
export const repositoryRoot = path.resolve(scriptDirectory, "..");

const buildOutputPattern = /^(?:public|public_new|public_temp|temp_public(?:_v\d+)?)$/;

export async function cleanupBuildOutputs() {
  const entries = await readdir(repositoryRoot, { withFileTypes: true });
  const outputNames = entries
    .filter(
      (entry) =>
        (entry.isDirectory() || entry.isSymbolicLink()) &&
        buildOutputPattern.test(entry.name),
    )
    .map((entry) => entry.name)
    .sort();

  if (outputNames.length === 0) {
    console.log("[clean] no build output directories found");
    return;
  }

  for (const outputName of outputNames) {
    const target = path.resolve(repositoryRoot, outputName);
    if (path.dirname(target) !== repositoryRoot) {
      throw new Error(`Refusing to remove a path outside the repository root: ${target}`);
    }

    await rm(target, {
      recursive: true,
      force: true,
      maxRetries: 3,
      retryDelay: 250,
    });
    console.log(`[clean] removed ${outputName}/`);
  }
}

const isMainModule =
  process.argv[1] &&
  pathToFileURL(path.resolve(process.argv[1])).href === import.meta.url;

if (isMainModule) {
  cleanupBuildOutputs().catch((error) => {
    console.error(`[clean] ${error.message}`);
    process.exitCode = 1;
  });
}
