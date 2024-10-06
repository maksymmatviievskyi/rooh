<script>
  import { cleanupConnection, initializeConnection } from "$lib/rtc";
  import { onMount, beforeUpdate, onDestroy } from "svelte";
  import store from "$lib/stores/workout";
  export let data;
  const workout = data.slug.split("+");

  onMount(() => {
    // Code to run on initial page load
    initializeConnection(store, workout);
  });

  beforeUpdate(() => {
    // Code to run before each update (e.g., page refresh)
    // Cancel the previous RTC connection and start a new one
    cleanupConnection();
  });

  onDestroy(() => {
    // Cleanup when the component is destroyed
    cleanupConnection();
  });
</script>

<div id="media" class="h-full">
  <!-- svelte-ignore a11y-media-has-caption -->
  <video id="video" autoplay="true" playsinline="true" class="h-full w-full"
  ></video>
</div>
