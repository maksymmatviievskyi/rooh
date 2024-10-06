<script>
  import { auth } from "$lib/stores/auth";
  import { page } from "$app/stores";
  import { logout } from "$lib/auth";
</script>

<header class="w-full flex flex-col items-center z-10 py-9 gap-6">
  <nav class="flex w-full justify-between">
    <div class="flex gap-5 items-center">
      <img src="logo.svg" alt="vprava logotype" class="invert w-14" />
      <a
        href="/home"
        class={$page.url.pathname == "/home"
          ? "text-black"
          : "text-neutral-500"}>home/</a
      >
      <a
        href="/progress"
        class={$page.url.pathname == "/progress"
          ? "text-black"
          : "text-neutral-500"}>progress/</a
      >
    </div>
    <div class="flex gap-5 items-center">
      <p>{$auth.username}</p>
      <button
        class="flex items-center gap-3 p-2 border-black border rounded"
        on:click={logout}
        >Log out <img src="logout-ico.svg" alt="icon" /></button
      >
    </div>
  </nav>
</header>
<slot />
<footer class="flex w-full justify-between gap-3 bg-black items-center">
  <a href="/"><img src="logo.svg" alt="rooh logo" /></a>
  <p class="text-neutral-500">by Maksym Matviievskyi</p>
</footer>
