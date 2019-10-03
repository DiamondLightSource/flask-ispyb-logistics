
<!--
Component that allows user to scan a barcode/facilityCode and update the dewar location
Emits an event if the updated is successful so the main page can refresh the list
Also updates the error/info messages held in the stores
-->
<template>
    <section>
        <h2 class="text-3xl text-center font-bold py-2">Scan Dewar and Rack</h2>
        <form>
            <div class="mb-3 px-2">
                <label class="block text-gray-700">Barcode or FacilityCode</label>
                <input ref="barcode" type="text" class="shadow appearance-none border rounded w-full py-1 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" v-model="barcode" v-on:keydown.enter="onBarcodeEnter" placeholder="Scan the long barcode from the dewar case">        
            </div>

            <div class="mb-3 px-2">
                <label class="block text-gray-700">Location</label>
                <input ref="location" type="text" class="shadow appearance-none border rounded w-full py-1 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" v-model="location" v-on:keydown.enter="onLocationEnter" placeholder="Scan the location e.g. RACK-A1">        
            </div>

            <div class="flex">
                <button type="submit" class="text-white bg-link hover:bg-blue-800 rounded p-1 m-2 w-1/2" v-on:click="onSetLocation">Submit</button>              
                <button type="cancel" class="text-white bg-info hover:bg-blue-600 rounded p-1 m-2 w-1/2"  v-on:click="onClearLocationForm">Cancel</button>
            </div>
        </form>
    </section>
</template>

<script>
import {Howl} from 'howler'

export default {
    name: 'ScanDewar',
    props: {
        msg: String,
        allowed_locations: Array,
    },
    data() {
        return {
            barcode: '',
            location: '',
        }
    },
    // Initialize the sound library and files
    created: function() {
        this.sounds = {}
        this.sounds.success = new Howl({
            src: ['/static/audio/success.mp3', '/static/audio/success.wav']
        });
        this.sounds.fail = new Howl({
            src: ['/static/audio/fail.mp3', '/static/audio/fail.wav']
        });
    },
    // Lifecycle hook - called when Vue is mounted on the page (trigger first get request)...
    mounted: function() {
        // When page is loaded set focus to the input location element
        this.$refs.barcode.focus();
    },
    methods: {
        onClearLocationForm: function() {
            console.log("on Clear Location Form")
        },
        // Prevent form submission and move focus to next input element
        onBarcodeEnter: function(event) {
            event.preventDefault()
            this.$refs.location.focus()
        },
        // Prevent form submission
        onLocationEnter: function(event) {
            event.preventDefault()
            if (this.barcode) {
                this.onSetLocation(event)
            }
        },

        // Method to update dewar location in database
        onSetLocation: function(event) {
            event.preventDefault()

            if (this.barcode && this.location) {
                // WE need to search for rack locations plus where the dewar might be sent (beamlines)
                // let full_locations = beamlines.concat(Object.keys(this.rack_locations))
                let hasLocation = this.allowed_locations.indexOf(this.location.toUpperCase())

                if (hasLocation < 0) {
                    // Something wrong - not a location we should set
                    let message = 'Error - location ' + this.location + ' not allowed for this page'
                    let isError = true
                    this.$store.dispatch("updateMessage", {text: message, isError: isError})

                    this.location = ''
                    this.playFail();
                    return
                }
                let formData = new FormData();
                formData.append('barcode', this.barcode)
                formData.append('location', this.location)

                // Store a reference to this for inner callbacks
                let self = this
                let barcode = this.barcode
                let location = this.location

                let url = this.$store.state.apiRoot + "dewars/locations"

                this.$http.post(url, formData)
                .then(function(response) {
                    let json = response.data
                    let message = ""
                    let isError = false

                    // Changed because we don't get the dewar id back from synchweb
                    // We get a DEWARHISTORYID instead
                    if ( json['DEWARHISTORYID'] > 0 ) {
                        message = "Updating " + barcode + " to " + location
                        self.isError = false
                        self.playSuccess();
                        // Inform Main Page so it can force a refresh
                        self.$emit("dewars-updated")
                    } else {
                        if (json['reason']) {
                            message = json['reason']
                        } else {
                            message = "Error - no dewar history id returned"                            
                        }
                        isError = true
                        self.playFail();
                    }
                    self.$store.dispatch("updateMessage", {text: message, isError: isError})
                })
                .catch(function() {
                    let message = "Error updating " + barcode + " to " + location
                    let isError = true
                    self.$store.dispatch("updateMessage", {text: message, isError: isError})
                    self.playFail();
                })
                // Reset form values
                this.barcode = ''
                this.location = ''
                // When submission occurs, set focus to the input barcode element
                this.$refs.barcode.focus();
            } else {
                // Information warning
                let message = "Issue with form: "
                if (this.barcode === "") {
                    message += " no barcode provided..."
                }
                if (this.location === "") {
                    message += ' no location provided...'
                }
                this.$store.dispatch('updateMessage', {text: message, isError: false})
            }                 
        },
        // Audio feedback methods
        playSuccess: function() {
            console.log("HAPPY BEEPS")
            this.sounds.success.play()
        },
        playFail: function() {
            console.log("SAD BEEPS")
            this.sounds.fail.play()
        },
    }
}
</script>