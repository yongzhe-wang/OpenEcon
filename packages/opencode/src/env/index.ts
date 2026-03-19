import { Instance } from "../project/instance"

export namespace Env {
  let state: (() => Record<string, string | undefined>) | undefined

  function current() {
    // Lazily initialize instance state to avoid module-evaluation cycles.
    // Accessing Instance.state at top-level can throw in circular import paths.
    if (!state) {
      state = Instance.state(() => {
        // Create a shallow copy to isolate environment per instance
        // Prevents parallel tests from interfering with each other's env vars
        return { ...process.env } as Record<string, string | undefined>
      })
    }
    return state()
  }

  export function get(key: string) {
    const env = current()
    return env[key]
  }

  export function all() {
    return current()
  }

  export function set(key: string, value: string) {
    const env = current()
    env[key] = value
  }

  export function remove(key: string) {
    const env = current()
    delete env[key]
  }
}
