<template>
    <div v-if="message" class="flex">
        <article class="w-full m-2 px-12 py-4 border-l-4" v-bind:class="[isError ? 'bg-red-100 border-red-400 text-red-700' : 'bg-blue-100 border-blue-400 text-blue-800']">
        <div class="text-xl">
          {{message}}
        </div>
      </article>
    </div>
</template>

<script>
export default {
    name: 'ErrorMessage',
    
    // Could use mapState in future (see Vuex)
    computed: {
        message() {
            return this.$store.state.message.text
        },
        isError() {
            return this.$store.state.message.isError
        }
    }
}
</script>