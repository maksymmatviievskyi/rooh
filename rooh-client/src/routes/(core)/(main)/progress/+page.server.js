export async function load({ fetch, cookies }) {
  const access = cookies.get("access") === "true";
  //   if (access) {
  const username = cookies.get("username");
  const response = await fetch("http://127.0.0.1:8080/sessions", {
    body: JSON.stringify({
      username,
    }),
    headers: {
      "Content-Type": "application/json",
    },
    method: "POST",
  });
  const data = await response.json();
  return {
    sessions: data.sessions,
  };
}
