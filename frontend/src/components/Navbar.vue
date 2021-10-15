<template>
  <div>
    <b-navbar toggleable="lg" type="dark" variant="dark">
    <b-navbar-brand href="#">Dragon-Controller</b-navbar-brand>

    <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

    <b-collapse id="nav-collapse" is-nav>

      <!-- Right aligned nav items -->
      <b-navbar-nav class="ml-auto">

        <b-nav-item-dropdown text="Kontrolle" right>
          <b-dropdown-item href="#">Licht</b-dropdown-item>
          <b-dropdown-item href="#">Sensoren</b-dropdown-item>
        </b-nav-item-dropdown>
        <b-nav-item-dropdown text="Tools" right>
          <b-dropdown-item href="#">Rechner</b-dropdown-item>
        </b-nav-item-dropdown>
      </b-navbar-nav>
    </b-collapse>
  </b-navbar>
  </div>
</template>

<script>
export default {
  name: "Navbar"
}
</script>

<style scoped>
  #brand {
    margin: 0 10px;
  }
</style>