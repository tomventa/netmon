<script>
  import {auth} from '../../utils/auth.js'
  import logo from '../../assets/logo.png'
  import "../../admin_lte/plugins/fontawesome-free/css/all.min.css"
  import "../../admin_lte/plugins/icheck-bootstrap/icheck-bootstrap.min.css"
  import "../../admin_lte/plugins/overlayScrollbars/css/OverlayScrollbars.min.css"
  import "../../admin_lte/dist/css/adminlte.min.css"
  import "../../admin_lte/plugins/jquery/jquery.min.js"
  import "../../admin_lte/plugins/bootstrap/js/bootstrap.bundle.min.js"
  import "../../admin_lte/plugins/overlayScrollbars/js/jquery.overlayScrollbars.min.js"
  import "../../admin_lte/dist/js/adminlte.js"

  let error = "";
  let dark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
  if (dark) document.body.classList.add("dark-mode");

  function handleSubmit(e){
    const dataRaw = new FormData(e.target);
    const dataJson = Object.fromEntries(dataRaw.entries());
    let response = auth.login(dataJson);
    response.then(res => {
      if (res.success){
        let confirm = auth.check();
        window.location.href = "/";
      }else{
        error = res.message;
      }
    });
  }
</script>


<main>
  <div class="login-box">
  <!-- /.login-logo -->
  <div class="card card-outline card-primary">
    <div class="card-header text-center">
      
      <a href="." class="h1">
        <img src={logo} class="img-fluid" width="50px" alt="logo">
        <b>net</b>mon
      </a>
    </div>
    <div class="card-body">
      {#if error!=""}
        <p class="login-box-msg">{error}</p>
      {/if}

      <form on:submit|preventDefault={handleSubmit}>
        <div class="input-group mb-3">
          <input type="text" name="username" class="form-control" placeholder="Username" 
                 required minlength="2" maxlength="64" pattern="[a-zA-Z0-9.-_]*">
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