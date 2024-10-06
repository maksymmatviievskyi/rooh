<script>
  import { register } from "$lib/auth";
  import { writable } from "svelte/store";
  let username = "";
  let password = "";
  let email = "";
  let chest = false;
  let hamstrings = false;
  let message = writable("");
</script>

<div class="flex flex-col gap-16 w-full">
  <div class="flex flex-col gap-3">
    <h1 class="text-4xl">Register</h1>
    <h2 class="text-neutral-500">Join our community now!</h2>
  </div>
  <h1 class="text-4xl">Please put your login info here.</h1>
  <form
    class="w-full flex flex-col gap-10"
    on:submit|preventDefault={() =>
      register(username, password, email, message, chest, hamstrings)}
  >
    <input
      class="border-b-2 text-3xl outline-none hover:border-black active:border-black hover:transition invalid:border-red-500 invalid:text-red-500"
      placeholder="Your username"
      type="text"
      id="username"
      bind:value={username}
    />
    <input
      class="border-b-2 text-3xl outline-none hover:border-black active:border-black hover:transition invalid:border-red-500 invalid:text-red-500"
      placeholder="Your email"
      type="email"
      id="email"
      bind:value={email}
    />
    <input
      class="border-b-2 text-3xl outline-none hover:border-black active:border-black hover:transition invalid:border-red-500 invalid:text-red-500"
      placeholder="Your password"
      type="password"
      id="password"
      bind:value={password}
    />
    <div class="flex flex-col gap-5">
      <h1 class="text-4xl">What do you want to focus on?</h1>
      <div class="flex gap-3">
        <input
          class="border-b-2 text-3xl outline-none hover:border-black active:border-black hover:transition invalid:border-red-500 invalid:text-red-500"
          type="checkbox"
          id="c1"
          bind:checked={hamstrings}
        />

        <label for="c1" class="text-3xl">Hamstrings</label>
      </div>
      <div class="flex gap-3">
        <input
          class="border-b-2 outline-none hover:border-black active:border-black hover:transition invalid:border-red-500 invalid:text-red-500"
          type="checkbox"
          id="c2"
          bind:checked={chest}
        />
        <label for="c2" class="text-3xl">Chest</label>
      </div>
    </div>
    <button
      type="submit"
      class="flex text-xl gap-3 items-center border border-black py-2 px-10 rounded w-fit group hover:transition"
    >
      Register <img
        class="group-hover:translate-x-1 transition"
        src="arrow-ico.svg"
        alt="icon"
      />
    </button>
  </form>
  <p class="text-2xl text-red-500">{$message}</p>
</div>
