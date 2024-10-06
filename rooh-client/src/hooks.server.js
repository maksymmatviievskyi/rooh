import { redirect } from "@sveltejs/kit";
import { auth, setUser } from "$lib/stores/auth";

/** @type {import('@sveltejs/kit').Handle} */
export async function handle({ event, resolve }) {
  const access = event.cookies.get("access") === "true";
  if (!access && event.route.id?.startsWith("/(core)")) {
    throw redirect(302, "/login");
  }
  if (access) {
    if (
      event.route.id?.startsWith("/(authentication)") ||
      event.route.id == "/"
    ) {
      throw redirect(302, "/home");
    }
    const username = event.cookies.get("username");
    setUser(username);

    const response = await fetch("http://127.0.0.1:8080/library", {
      body: JSON.stringify({
        username,
      }),
      headers: {
        "Content-Type": "application/json",
      },
      method: "POST",
    });
    // Check whether the exercise exists in the user library, otherwise redirect
    const data = await response.json();
    const exerciseNames = data?.exerciseNames.flat();
    const path = event.url.pathname;
    if (
      path.includes("/start/") &&
      !exerciseNames.some((o) => path.includes(o))
    ) {
      throw redirect(302, "/home");
    }
  }

  const response = await resolve(event);
  return response;
}
