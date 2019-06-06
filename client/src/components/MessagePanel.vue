<template>
    <div v-if="message" class="columns">
        <article class="column is-12 message" v-bind:class="[isError ? 'is-danger' : 'is-info']">
        <div class="message-body subtitle">
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