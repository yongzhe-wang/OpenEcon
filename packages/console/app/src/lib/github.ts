"use server"

export async function github() {
  return {
    stars: 0,
    release: undefined as { tag: string; url: string } | undefined,
    contributors: 0,
  }
}
