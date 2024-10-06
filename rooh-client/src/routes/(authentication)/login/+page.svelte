<script>
  import { login } from "$lib/auth";
  import { writable } from "svelte/store";
  let email = "";
  let password = "";
  let message = writable("");
</script>

<div class="flex flex-col gap-16 w-full">
  <h1 class="text-4xl">Login</h1>
  <h1 class="text-4xl">Please put your login info here.</h1>
  <form
    class="w-full flex flex-col gap-10"
    on:submit|preventDefault={() => login(email, password, message)}
  >
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
      invali
      type="password"
      id="password"
      bind:value={password}
    />
    <button
      type="submit"
      class="flex text-xl gap-3 items-center border border-black py-2 px-10 rounded w-fit group hover:transition"
    >
      Enter <img
        class="group-hover:translate-x-1 transition"
        src="arrow-ico.svg"
        alt="icon"
      />
    </button>
  </form>
  <p class="text-2xl text-red-500">{$message}</p>
</div>
