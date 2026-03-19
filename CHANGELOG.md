# Changelog

## 2026-03-19
- Fixed broken dependency source in `packages/app/package.json` by restoring `ghostty-web` to `github:anomalyco/ghostty-web#main` so `bun install` can resolve.
- Added structured worker startup error logging in `packages/opencode/src/cli/cmd/tui/thread.ts` to expose real crash causes.
- Fixed circular-import startup crash by lazily initializing env state in `packages/opencode/src/env/index.ts`.
- Fixed circular-import startup crash by lazily initializing config state in `packages/opencode/src/config/config.ts`.
- Made `.github/TEAM_MEMBERS` optional in `packages/script/src/index.ts` so desktop predev/build works after attribution file removal.
- Updated `packages/desktop/scripts/predev.ts` to force `OPENCODE_CHANNEL=local` and `OPENCODE_VERSION=local` during sidecar builds, preventing unresolved `@opencode-ai/plugin@0.0.0-dev-*` installs in local desktop dev.
- Updated shared UI branding component in `packages/ui/src/components/logo.tsx` so `Mark`, `Splash`, and `Logo` render the new `E` mark and OpenEcon wordmark geometry in desktop/app views.
- Regenerated desktop dev icon assets in `packages/desktop/src-tauri/icons/dev/*` to use a green background with a white `E` mark, including rebuilt `icon.icns` for macOS Dock.
- Added `packages/desktop/scripts/generate_dev_icons.py` utility to reproducibly regenerate the green OpenEcon dev icon set.
