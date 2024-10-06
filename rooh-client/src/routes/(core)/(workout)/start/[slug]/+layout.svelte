<script>
  import store from "$lib/stores/workout";
  import { time } from "$lib/stores/workout";
  import { goto } from "$app/navigation";
  import { fly } from "svelte/transition";
  import { pc, cleanupConnection } from "$lib/rtc";
  import { onDestroy, onMount } from "svelte";
  let { count, detection, feedback, finished } = store;
  let pausedProgram;
  let timerInterval;
  let startTime = Date.now();
  let elapsedTime = 0;
  let animate = false;
  onMount(() => {
    startTimer();
    animate = true;
  });

  onDestroy(() => {
    terminateTimer();
  });

  finished.subscribe((value) => {
    if (value) {
      console.log("Redirecting...");
      setTimeout(() => {
        finished.set(false);
        goto("/home");
      }, 3000);
    }
  });

  function cancel() {
    cleanupConnection();
    terminateTimer();
    goto("/home");
  }

  function pause() {
    pausedProgram = true;
    pc.getSenders().forEach((sender) => {
      const parameters = sender.getParameters();
      parameters.encodings[0].active = false;
      sender.setParameters(parameters);
    });
    pauseTimer();
  }
  function resume() {
    pausedProgram = false;
    pc.getSenders().forEach((sender) => {
      const parameters = sender.getParameters();
      parameters.encodings[0].active = true;
      sender.setParameters(parameters);
    });
    startTimer();
  }

  function startTimer() {
    startTime -= -elapsedTime;
    timerInterval = setInterval(updateTime, 1000);
  }

  function updateTime() {
    let currentTime = Date.now();
    elapsedTime = Math.round((currentTime - startTime) / 1000);
    time.set(formatTime(elapsedTime));
  }

  function pauseTimer() {
    clearInterval(timerInterval);
    pausedProgram = true;
  }

  function terminateTimer() {
    clearInterval(timerInterval);
    time.set(0);
  }

  function formatTime(t) {
    let min = Math.floor(t / 60);
    let sec = t % 60;
    return `${min < 10 ? "0" + min : min}:${sec < 10 ? "0" + sec : sec}`;
  }
</script>

<div class="h-screen flex flex-col justify-between">
  <header
    class="text-white w-full flex flex-col items-center z-10 absolute py-9 px-6 gap-6"
  >
    <nav class="flex w-full justify-between px-9">
      <div class="flex flex-col gap-3 items-center">
        <p>Reps</p>
        <p class="font-bold">{$count}</p>
      </div>
      <div class="flex flex-col gap-3 items-center">
        <p id="workoutDuration">Elapsed</p>
        <p class="font-bold">{$time}</p>
      </div>
      <div class="flex flex-col gap-3 items-center">
        <p>Class</p>
        <p class="font-bold">{$detection}</p>
      </div>
    </nav>

    <p
      class="max-w-full w-fit px-6 py-1 rounded backdrop-blur-md bg-black text-5xl"
    >
      {$feedback}
    </p>
  </header>
  {#if $finished}
    <div
      class="absolute flex w-full h-full bg-white justify-center items-center"
    >
      <p class="text-black">Complete!</p>
    </div>
  {/if}
  <slot />
  <footer class="absolute bottom-0 flex w-full justify-center p-6 gap-3">
    {#if pausedProgram}
      <button
        on:click={resume}
        class="flex justify-center items-center bg-black p-2 rounded w-9"
      >
        <img src="/resume.svg" alt="voice ico" class="invert" />
      </button>
    {:else}
      <button
        on:click={pause}
        class="flex justify-center items-center bg-black p-2 rounded w-9"
      >
        <img src="/pause.svg" alt="voice ico" class="invert" />
      </button>
    {/if}
    <button
      on:click={cancel}
      class="flex justify-center items-center bg-black p-2 rounded w-9"
    >
      <img src="/dismiss.svg" alt="voice ico" class="invert" />
    </button>
  </footer>
</div>
