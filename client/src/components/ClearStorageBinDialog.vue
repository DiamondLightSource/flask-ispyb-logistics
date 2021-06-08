<!--
Modal Dialog Box to confirm removal of all containers from a storage bin
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
            <section class="p-4 flex flex-col">
                <p class="mb-2">Confirm removal of all containers from {{storageBin}}?</p>
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
    name: 'ClearStorageBinDialog',
    props: {
        isActive: {
            type: Boolean,
            required: true
        },
        storageBin: {
            type: String,
            required: true
        },
        containers: {
            type: Array,
            default: function() { return [] }
        }
    },
    methods: {
        // User has confirmed to remove the dewar from this location
        onConfirm: function() {
            // Store variables for use within axios handler functions
            let location = 'removed-from-'+this.storageBin

            this.containers.forEach( (container) => {
                console.log("Remove container for id " + container)
                this.updateContainerLocation(container, location)
            })
        },
        // User has cancelled or location is invalid and the request has been rejected        
        onClose: function() {
            this.$emit("confirm-removal", false)
        },

        updateContainerLocation: function(containerId, location) {
            let self = this
            let url = this.$store.state.apiRoot + "containers/locations"

            let formData = new FormData();
            formData.append('containerId', containerId)
            formData.append('location', location)

            this.$http.post(url, formData)
            .then(function() {
                let message = "Updating container " + containerId + " from location " + location + "..."
                self.$store.dispatch("updateMessage", {text: message, isError: false})
            })
            .catch(function() {
                let message = "Error removing container " + containerId + " from location " + location
                self.$store.dispatch("updateMessage", {text: message, isError: true})
            })
            this.$emit("confirm-removal", true)
        }
    }
}
</script>