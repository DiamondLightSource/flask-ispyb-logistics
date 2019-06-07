<template>
  <div id="app">
    <Home/>
  </div>
</template>


<script>
import Home from './views/Home.vue'

export default {
	name: 'App',
	components: {
		Home
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
