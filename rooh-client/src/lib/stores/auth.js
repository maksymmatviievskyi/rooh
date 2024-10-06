import { writable } from "svelte/store";

export const auth = writable({
  isAuthenticated: false,
  username: null,
});

export const setUser = (username) => {
  auth.update((state) => ({ ...state, isAuthenticated: true, username }));
};

export const clearUser = () => {
  auth.update((state) => ({
    ...state,
    isAuthenticated: false,
    username: null,
  }));
};
