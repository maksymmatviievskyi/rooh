<script>
  import { auth } from "$lib/stores/auth";
  export let data;
  let link = "";
</script>

<div class="flex flex-col gap-10 h-full">
  <div class="flex flex-col gap-3">
    <h2 class="text-4xl">Howdy, {$auth.username}</h2>
    <h3 class="text-neutral-500">Start a workout now!</h3>
  </div>
  <div class="flex flex-col gap-3">
    <p class="text-neutral-500">Choose your workout first</p>
    <div class="flex gap-5">
      {#each data.exercises as name}
        <div class="flex flex-col border border-white rounded">
          <span
            class={link === name ? "underline" : ""}
            on:click={() => {
              link = name;
            }}
          >
            {name}
          </span>
        </div>
      {/each}
    </div>
    <a href="/start/{link}" class="text-9xl">Start now</a>
  </div>
</div>
