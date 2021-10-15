<template>
  <div id="app">
    <navbar></navbar>
    <humidity-calculator></humidity-calculator>
  </div>
</template>

<script>
import HumidityCalculator from "./components/HumidityCalculator";
import Navbar from "./components/Navbar";

export default {
  name: 'App',
  components: {
    Navbar,
    HumidityCalculator
  }
}
</script>

<style>
#app {
}
</style>
