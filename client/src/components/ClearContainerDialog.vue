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
            <section class="p-4 flex flex-col">
            <p class="mb-2">Confirm removal of container id {{containerId}} from {{locationToRemove}}?</p>
            <div class="">
                <label class="mr-2">Is Container moving to beamline?</label>
                <input class="mr-2" type="checkbox" v-model="toBeamline"/><span v-if="toBeamline">Yes</span><span v-else>No</span>
            </div>
            <div v-if="toBeamline">
                <label for="beamline" class="mr-2">Select Beamline if container will be moved there</label>
                <input type="text" list="beamlines" id="beamline" v-model="beamline" class="shadow appearance-none border rounded px-1 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"/>
                <datalist id="beamlines">
                    <option v-for="bl in beamlines" :key="bl">{{bl}}</option>
                </datalist>
            </div>
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
    name: 'ClearContainerDialog',
    props: {
        isActive: {
            type: Boolean,
            required: true
        },
        containerId: {
            type: Number,
            required: true
        },
        locationToRemove: {
            type: String,
            required: true
        }
    },
    data() {
        return {
            toBeamline: false,
            beamline: '',
        }
    },
    computed: {
        beamlines: function() {
            return this.$store.state.beamlines
        }
    },
    methods: {
        resetForm: function() {
            this.beamline = ''
            this.toBeamline = false
        },
        // User has confirmed to remove the dewar from this location
        onConfirm: function() {
            // Store variables for use within axios handler functions
            let location = this.getTargetLocation()

            if (location === null) {
                this.$store.dispatch("updateMessage", {text: 'Invalid location entered, container not removed from ' + this.locationToRemove, isError: true})
                this.onClose()
            } else {
                this.updateContainerLocation(this.containerId, location)
            }
        },
        getTargetLocation: function() {
            // The target location is either empty (if cleared) or a valid beamline
            let location = !this.toBeamline ? 'removed-from-'+this.locationToRemove : null

            if (this.toBeamline && this.isBeamlineValid()) location = this.beamline

            return location
        },
        isBeamlineValid: function() {
            // If beamline is in the list then all good too.
            if (this.beamlines.indexOf(this.beamline) > -1 ) return true
            // At this point, the user has entered an unexpected value
            return false
        },
        // User has cancelled or location is invalid and the request has been rejected        
        onClose: function() {
            this.$emit("confirm-removal", false)
            this.resetForm()
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
            this.resetForm()
        }
    }
}
</script>