import { setUser, clearUser } from "$lib/stores/auth";
import { goto } from "$app/navigation";

export async function login(email, password, message) {
  const response = await fetch("http://127.0.0.1:8080/login", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ email, password }),
  });

  if (response.ok) {
    const data = await response.json();
    setUser(data.username);
    cookieStore.set("access", true);
    cookieStore.set("username", data.username);
    goto("/home");
  } else if (response.status === 404) {
    message.set("User doesn't exist!");
  } else if (response.status === 403) {
    message.set("Wrong password!");
  } else {
    message.set("Login failed!");
  }
}

export async function logout() {
  clearUser();
  await cookieStore.getAll().then((cookies) =>
    cookies.forEach((cookie) => {
      cookieStore.delete(cookie);
    })
  );

  await goto("/login");
}

function validInputs(username, password, email, message) {
  // Validate username
  if (username.trim() === "" || username.includes(" ")) {
    message.set("Username cannot be empty or contain spaces.");
    return false;
  }

  // Validate password
  if (password.length < 6 || password.includes(" ")) {
    message.set(
      "Password must be at least 6 characters long and cannot contain spaces."
    );
    return false;
  }

  // Validate email
  const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!email.match(emailPattern)) {
    message.set("Email is invalid.");
    return false;
  }

  message.set("Registration successful. Redirecting ...");
  return true;
}

export async function register(
  username,
  password,
  email,
  message,
  chest,
  hamstrings
) {
  if (validInputs(username, password, email, message)) {
    const response = await fetch("http://127.0.0.1:8080/register", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ username, email, password, chest, hamstrings }),
    });

    if (response.ok) {
      message.set("");
      goto("/login");
    } else if (response.status === 403) {
      message.set("This username is taken");
    } else {
      message.set("An server error occurred");
    }
  }
}
