import { $ } from "bun"

import { copyBinaryToSidecarFolder, getCurrentSidecar, windowsify } from "./utils"

const RUST_TARGET = Bun.env.TAURI_ENV_TARGET_TRIPLE

const sidecarConfig = getCurrentSidecar(RUST_TARGET)

const binaryPath = windowsify(`../opencode/dist/${sidecarConfig.ocBinary}/bin/opencode`)

// Force local build metadata for desktop dev sidecar builds.
// This prevents generated dev snapshot versions (0.0.0-dev-*) from being used
// to resolve @opencode-ai/plugin from npm during local workspace runs.
process.env.OPENCODE_CHANNEL = "local"
process.env.OPENCODE_VERSION = "local"

await (sidecarConfig.ocBinary.includes("-baseline")
  ? $`cd ../opencode && bun run build --single --baseline`
  : $`cd ../opencode && bun run build --single`)

await copyBinaryToSidecarFolder(binaryPath, RUST_TARGET)
