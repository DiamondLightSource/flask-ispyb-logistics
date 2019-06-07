<template>
  <div id="app">
    <Dewars zone="zone6"></Dewars>
  </div>
</template>

<script>
import Dewars from '../../views/Dewars.vue'

export default {
  name: 'zone6',
  components: {
    Dewars
  }
}
</script>

<style>
.container-fluid {
  padding: 20px;
}

div.solid-border {
  border-style: solid;
  border-width: 1px 1px 1px 1px;
}

div.box {
  cursor: pointer;
}


</style>
