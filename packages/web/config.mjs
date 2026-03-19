const stage = process.env.SST_STAGE || "dev"

export default {
  url: stage === "production" ? "https://openecon.ai" : `https://${stage}.openecon.ai`,
  console: stage === "production" ? "https://openecon.ai/auth" : `https://${stage}.openecon.ai/auth`,
  email: "contact@openecon.ai",
  socialCard: "https://social-cards.sst.dev",
  github: "https://github.com/openecon/opencode",
  discord: "https://openecon.ai/discord",
  headerLinks: [
    { name: "app.header.home", url: "/" },
    { name: "app.header.docs", url: "/docs/" },
  ],
}
