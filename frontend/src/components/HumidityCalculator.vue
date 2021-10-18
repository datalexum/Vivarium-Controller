<template>
  <div>
    <b-alert
        :show="dismissCountDown"
        variant="danger"
        @dismissed="dismissCountDown=0"
        @dismiss-count-down="countDownChanged">
      You need to supply exactly two values!
    </b-alert>
    <div id="form">
        <b-form>
          <b-form-group class="flex-row">
            <label>Relative Humidity (%): </label>
            <input v-model="rel"/>
          </b-form-group >
          <b-form-group class="flex-row">
            <label>Absolute Humidity: </label>
            <input v-model="abs"/>
          </b-form-group>
          <b-form-group class="flex-row">
            <label>Temperature (°C): </label>
            <input v-model="temp"/>
          </b-form-group>
          <b-button @click="clicker" id="submit">Calculate</b-button>
        </b-form>
    </div>
  </div>

</template>

<script>
export default {
  name: "HumidityCalculator",
  methods: {
    clicker: function () {
      if ((!this.rel + !this.temp + !this.abs) == 1) {
        alert("H");
      } else {
        this.dismissCountDown = this.dismissSecs
      }
    },
    countDownChanged: function (dismissCountDown) {
        this.dismissCountDown = dismissCountDown
      }
  },
  data() {
    return {
      rel: '',
      abs: '',
      temp: '',
      dismissSecs: 2,
      dismissCountDown: 0
    };
  }

}
</script>

<style scoped>
  #form{
    width: 230px;
    flex-grow: inherit;
    margin: auto;
    margin-top: 20px;

  }
  .flex-row{
    display: flex;
    width: 100%;
  }
  #submit {
    margin-top: 20px;
  }
</style>