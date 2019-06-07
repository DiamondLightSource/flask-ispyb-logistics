<template>
  <div id="app">
    <Stores></Stores>
  </div>
</template>

<script>
import Stores from '../../views/Stores.vue'

export default {
  name: 'stores',
  components: {
    Stores
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
