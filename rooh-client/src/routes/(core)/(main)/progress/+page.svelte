<script>
  export let data;
  let exerciseTypes = [...new Set(data.sessions.map((sesh) => sesh[2]))];
  function calcProgress(a, b) {
    return Math.round((b / a - 1) * 100);
  }
</script>

<div class="h-full flex flex-col gap-10 mb-9">
  <div class="flex flex-col gap-3">
    <h2 class="text-4xl">Progress</h2>
    <h3 class="text-neutral-500">Check out how much you have done, Maksym!</h3>
  </div>
  <div class="flex flex-col gap-10">
    {#each exerciseTypes as exerciseType}
      <div class="flex flex-col gap-3 justify-centre w-full">
        <div class="flex gap-5">
          <h2 class="text-xl">{exerciseType}</h2>
          <p>
            {calcProgress(
              ...data.sessions
                .filter((session) => session.includes(exerciseType))
                .map(([reps, exercise]) => reps)
            )}% increase
          </p>
        </div>
        <div class="flex gap-2">
          {#each data.sessions.filter((item) => item[2] === exerciseType) as [repetitions, date]}
            <div class="flex flex-col min-w-[150px] flex-1">
              <p>
                {new Date(date).toLocaleDateString("en-GB", {
                  day: "numeric",
                  month: "short",
                })}
              </p>
              <div class="bg-black p-1 text-white">{repetitions}</div>
            </div>
          {/each}
        </div>
      </div>
    {/each}
  </div>
</div>
