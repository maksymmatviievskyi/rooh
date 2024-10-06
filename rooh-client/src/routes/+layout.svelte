<script>
  import "../app.css";
  import { onMount } from "svelte";
  import { setUser } from "$lib/stores/auth";
  onMount(async () => {
    let ses = await cookieStore.get("username");
    if (ses) {
      setUser(ses.value);
    }
  });
</script>

<slot />
