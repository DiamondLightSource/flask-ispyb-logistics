<!--
Modal Dialog Box to confirm removal of a dewar from a location

Emits an event 'confirm-removal' with a boolean true/false if user confirmed action
-->
<template>
    <!-- This pops up to confirm the clear location action -->
    <div class="modal" v-bind:class="{ 'is-active' : isActive }">
      <div class="modal-background"></div>
      <div class="modal-card">
        <header class="modal-card-head">
          <p class="modal-card-title">Confirm Clear</p>
        </header>
        <section class="modal-card-body">
          <p>Confirm removal of dewar from location {{locationToRemove}}?</p>
        </section>
        <footer class="modal-card-foot">
          <button class="button is-success" v-on:click="onConfirmClear(true)">Confirm</button>
          <button class="button" v-on:click="onConfirmClear(false)">Cancel</button>
        </footer>
      </div>
    </div>

</template>

<script>
export default {
    name: 'ClearLocationDialog',
    props: ['isActive', 'locationToRemove', 'rack_locations'],
    methods: {
        // User has either confirmed or cancelled
        onConfirmClear: function(confirm) {
            if (confirm === true) {
                // Extra check to ensure this is a valid location
                let hasLocation = this.rack_locations.hasOwnProperty(this.locationToRemove)

                if (hasLocation) {
                    // Store variables for use within axios handler functions
                    let self = this
                    let barcode = this.rack_locations[this.locationToRemove]['barcode']
                    let url = this.$store.state.apiRoot + "dewars/locations"

                    this.$http.delete(url, {params: {'location': this.locationToRemove}})
                    .then(function(response) {
                        console.log(response)
                        let message = "Dewar removed " + barcode + " from location " + self.locationToRemove

                        this.$store.dispatch("updateMessage", {text: message, isError: false})
                    })
                    .catch(function() {
                        let message = "Error removing dewar " + barcode + " from location " + self.locationToRemove

                        self.$store.dispatch("updateMessage", {text: message, isError: true})
                    })
                }
            }
            this.$emit("confirm-removal", confirm)
        },
    }
}
</script>