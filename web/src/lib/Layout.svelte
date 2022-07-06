<script>
    export let currentPage;
    import Header from "./Header.svelte"
    import "../admin_lte/plugins/fontawesome-free/css/all.min.css"
    import "../admin_lte/plugins/icheck-bootstrap/icheck-bootstrap.min.css"
    import "../admin_lte/plugins/overlayScrollbars/css/OverlayScrollbars.min.css"
    import "../admin_lte/dist/css/adminlte.min.css"
    import "../admin_lte/plugins/jquery/jquery.min.js"
    import "../admin_lte/plugins/bootstrap/js/bootstrap.bundle.min.js"
    import "../admin_lte/plugins/overlayScrollbars/js/jquery.overlayScrollbars.min.js"
    import "../admin_lte/dist/js/adminlte.js"

</script>

<Header />

<main>
    <slot />
</main>
