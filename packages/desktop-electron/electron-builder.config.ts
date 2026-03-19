import type { Configuration } from "electron-builder"

const channel = (() => {
  const raw = process.env.OPENCODE_CHANNEL
  if (raw === "dev" || raw === "beta" || raw === "prod") return raw
  return "dev"
})()

const getBase = (): Configuration => ({
  artifactName: "openecon-electron-${os}-${arch}.${ext}",
  directories: {
    output: "dist",
    buildResources: "resources",
  },
  files: ["out/**/*", "resources/**/*"],
  extraResources: [
    {
      from: "resources/",
      to: "",
      filter: ["opencode-cli*"],
    },
    {
      from: "native/",
      to: "native/",
      filter: ["index.js", "index.d.ts", "build/Release/mac_window.node", "swift-build/**"],
    },
  ],
  mac: {
    category: "public.app-category.developer-tools",
    icon: `resources/icons/icon.icns`,
    hardenedRuntime: true,
    gatekeeperAssess: false,
    entitlements: "resources/entitlements.plist",
    entitlementsInherit: "resources/entitlements.plist",
    notarize: true,
    target: ["dmg", "zip"],
  },
  dmg: {
    sign: true,
  },
  protocols: {
    name: "OpenEcon",
    schemes: ["openecon"],
  },
  win: {
    icon: `resources/icons/icon.ico`,
    target: ["nsis"],
  },
  nsis: {
    oneClick: false,
    allowToChangeInstallationDirectory: true,
    installerIcon: `resources/icons/icon.ico`,
    installerHeaderIcon: `resources/icons/icon.ico`,
  },
  linux: {
    icon: `resources/icons`,
    category: "Development",
    target: ["AppImage", "deb", "rpm"],
  },
})

function getConfig() {
  const base = getBase()

  switch (channel) {
    case "dev": {
      return {
        ...base,
        appId: "ai.openecon.desktop.dev",
        productName: "OpenEcon Dev",
        rpm: { packageName: "openecon-dev" },
      }
    }
    case "beta": {
      return {
        ...base,
        appId: "ai.openecon.desktop.beta",
        productName: "OpenEcon Beta",
        protocols: { name: "OpenEcon Beta", schemes: ["openecon"] },
        publish: undefined,
        rpm: { packageName: "openecon-beta" },
      }
    }
    case "prod": {
      return {
        ...base,
        appId: "ai.openecon.desktop",
        productName: "OpenEcon",
        protocols: { name: "OpenEcon", schemes: ["openecon"] },
        publish: undefined,
        rpm: { packageName: "openecon" },
      }
    }
  }
}

export default getConfig()
