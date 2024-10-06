<script>
  import { page } from "$app/stores";
</script>

<div class="h-screen flex justify-center items-center flex-col gap-10">
  <h1 class="text-7xl text-center">Oooppppsie</h1>
  <p class="text-2xl text-center">
    Error <span class="font-black">{$page.error.message}</span> has occured
  </p>
</div>
