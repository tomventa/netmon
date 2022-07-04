<script>
  import {} from '../../utils/auth.js'

  let error = "";
  let dark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
  if (dark) document.body.classList.add("dark-mode");
</script>


<main>
  <div class="login-box">
  <!-- /.login-logo -->
  <div class="card card-outline card-primary">
    <div class="card-header text-center">
      <a href="." class="h1"><b>net</b>mon</a>
    </div>
    <div class="card-body">
      {#if error!=""}
        <p class="login-box-msg">{error}</p>
      {/if}

      <form action="#send" method="post">
        <div class="input-group mb-3">
          <input type="text" name="username" class="form-control" placeholder="Username" 
                 required minlength="2" maxlength="64" pattern="[a-zA-Z0-9\.\-\_]*">
          <div class="input-group-append">
            <div class="input-group-text">
              <span class="fas fa-user"></span>
            </div>
          </div>
        </div>
        <div class="input-group mb-3">
          <input type="password" name="password" class="form-control" placeholder="Password" 
                 required minlength="6" maxlength="128">
          <div class="input-group-append">
            <div class="input-group-text">
              <span class="fas fa-lock"></span>
            </div>
          </div>
        </div>
        <div class="row">
          <div class="col-8">
            <div class="icheck-primary">
              <input type="checkbox" id="remember">
              <label for="remember">
                Remember Me
              </label>
            </div>
          </div>
          <!-- /.col -->
          <div class="col-4">
            <button type="submit" class="btn btn-primary btn-block">Login</button>
          </div>
          <!-- /.col -->
        </div>

        <p class="mb-1">
          <a href="forgot-password.html">I forgot my password</a>
        </p>
      </form>
    </div>
    <!-- /.card-body -->
  </div>
  <!-- /.card -->
</div>
</main>