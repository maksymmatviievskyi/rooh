import { redirect } from "@sveltejs/kit";

export async function load(event) {
  const access = event.cookies.get("access") === "true";
  if (access && event.route.id?.startsWith("/(authentication)")) {
    throw redirect(302, "/home");
  }
}
