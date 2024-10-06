// store.js
import { writable } from "svelte/store";

// Create a writable store with an initial values
const store = {
  count: writable(0),
  detection: writable(""),
  feedback: writable([]),
  finished: writable(false),
};
export const time = writable("0:00");
export default store;
