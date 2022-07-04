<script>
  import  '../../public/js/auth.js'
  import {apiBase} from '../utils/api.js'
  let counter = 0;
  setInterval(function() {
    counter += 1;
  }, 1000)
</script>

<main>
  <h1>Hello world! {counter}</h1>

  <p>
    Visit <a href="https://svelte.dev">svelte.dev</a> to learn how to build Svelte
    apps.
  </p>

  <p>
    Check out <a href="https://github.com/sveltejs/kit#readme">SvelteKit</a> for
    the officially supported framework, also powered by Vite!
  </p>
</main>
