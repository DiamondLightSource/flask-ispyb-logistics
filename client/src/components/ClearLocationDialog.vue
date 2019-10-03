<!--
Modal Dialog Box to confirm removal of a dewar from a location

Emits an event 'confirm-removal' with a boolean true/false if user confirmed action
-->
<template>
    <!-- This pops up to confirm the clear location action -->
    <div v-if="isActive" 
        class="fixed inset-0 w-full h-screen flex items-center justify-center bg-semi-75"
        v-on:click.self="onClose()">
        <button
            aria-label="close"
            class="absolute top-0 right-0 text-xl text-gray-500 font-bold my-2 mx-4" 
            @click.prevent="onClose()">x</button>
      <div class="w-full max-w-2xl bg-white shadow-lg rounded-lg p-4">
        <header class="border-b-2">
            <h1 class="text-xl">Confirm Clear</h1>
            </header>
        <section class="p-4">
          <p>Confirm removal of dewar from location {{locationToRemove}}?</p>
        </section>
        <footer class="flex border-t-2">
          <button class="w-1/2 text-white bg-success hover:bg-green-700 rounded p-1 m-2" v-on:click="onConfirm()">Confirm</button>
          <button class="w-1/2 text-white bg-danger hover:bg-red-700 rounded p-1 m-2" v-on:click="onClose()">Cancel</button>
        </footer>
      </div>
    </div>

</template>

<script>
export default {
    name: 'ClearLocationDialog',
    props: ['isActive', 'locationToRemove', 'rack_locations'],
    methods: {
        // User has confirmed to remove the dewar from this location
        onConfirm: function() {
            // Extra check to ensure this is a valid location
            let hasLocation = this.rack_locations.hasOwnProperty(this.locationToRemove)

            if (hasLocation) {
                // Store variables for use within axios handler functions
                let self = this
                let location = this.locationToRemove
                let barcode = this.rack_locations[location]['barcode']
                let url = this.$store.state.apiRoot + "dewars/locations"

                this.$http.delete(url, {params: {'location': location}})
                .then(function(response) {
                    console.log(response)
                    let message = "Removing dewar " + barcode + " from location " + location + "..."

                    self.$store.dispatch("updateMessage", {text: message, isError: false})
                })
                .catch(function() {
                    console.log("Error removing dewar")
                    let message = "Error removing dewar " + barcode + " from location " + location

                    self.$store.dispatch("updateMessage", {text: message, isError: true})
                })
            }
            this.$emit("confirm-removal", true)
        },
        // User has cancelled        
        onClose: function() {
            this.$emit("confirm-removal", false)
        }
    }
}
</script>