<template>
  <div class="stores">
        <div class="">

            <!-- First set of columns are the top form elements -->
            <div class="flex flex-col sm:flex-row">

                <!-- Form element to set locations -->
                <div class="w-1/2 border border-solid border-black m-2 p-2">
                    <h2 class="text-3xl text-center font-bold">Scan Dewar and Barcode</h2>

                    <form>
                        <div class="mb-3 px-2">
                            <label class="block text-gray-700">Location</label>
                            <input ref="location" type="text" class="shadow appearance-none border rounded w-full py-1 px-3 text-gray-700 leading-tight focus:outline-none focus:ring" v-model="location" v-on:keydown.enter="onLocationEnter" placeholder="Scan the location e.g. STORES-IN or STORES-OUT">
                        </div>

                        <div class="mb-3 px-2">
                            <label class="block text-gray-700">Barcode</label>
                            <input ref="barcode" type="text" class="shadow appearance-none border rounded w-full py-1 px-3 text-gray-700 leading-tight focus:outline-none focus:ring" v-model="barcode" v-on:keydown.enter="onBarcodeEnter" placeholder="Scan the QR code / barcode from the dewar case">
                        </div>

                        <!-- If location is STORES-IN do not show AWB field...-->
                        <div v-show="location.toUpperCase() != 'STORES-IN'" class="mb-3 px-2">
                            <label class="block text-gray-700">Airway Bill</label>
                            <input ref="awb" type="text" class="shadow appearance-none border rounded w-full py-1 px-3 text-gray-700 leading-tight focus:outline-none focus:ring" v-model="awb" v-on:keydown.enter="onAwbEnter" placeholder="Scan the DHL / FedEx Airway Bill">
                        </div>
                    
                        <div class="flex">
                            <button type="submit" class="text-white bg-link hover:bg-blue-800 rounded p-1 m-2 w-1/2" v-on:click="onSetLocation">Submit</button>              
                            <button type="cancel" class="text-white bg-info hover:bg-blue-600 rounded p-1 m-2 w-1/2"  v-on:click="onClearLocationForm">Cancel</button>
                        </div>        
                    </form>

                </div>


                <div class="w-1/2 border border-solid border-black m-2 p-2 "> <!-- STORES LOCATIONS  -->
                    <h2 class="text-3xl text-center font-bold">Locations</h2>
                    <br />
                    <div class="flex">
                        <div class="w-1/2 mt-4">
                            <div class="flex-col text-center">
                                <div class="">
                                    <img class="inline-block" width=96 src='../assets/img/stores-in.gif'>
                                </div>
                               <p class="">STORES-IN</p>  
                            </div>
                        </div>
                        <div class="w-1/2 mt-4">
                            <div class="flex-col text-center">
                                <div class="">
                                    <img class="inline-block" width=96 src='../assets/img/stores-out.gif'>
                                </div>
                                <p class="">STORES-OUT</p>
                            </div>
                        </div>
                    </div>   
                </div> <!-- END STORES LOCATIONS -->


            </div> <!-- End of columns -->

            <!-- 
                Area for messages from back end 
                Currently conditional render based on error or warning
            -->
            <div v-if="message" class="flex">
                <article class="w-full m-2 px-12 py-4 border-l-4" v-bind:class="[isError ? 'bg-red-100 border-red-400 text-red-700' : 'bg-blue-100 border-blue-400 text-blue-800']">
                    <div class="text-xl">
                    {{message}}
                    </div>
                </article>
            </div>

        </div> <!-- END container fluid -->

        <!-- Display the stores history -->
        <div class="flex flex-col m-2 p-2">
            <h1 class="text-3xl font-bold text-center p-4">History</h1>
            <table class="border border-solid bg-white w-full">
                <thead class="text-left bg-white-300 font-bold border border-solid">
                    <th class="border px-3 py-2">Date/Time</th><th class="border px-3 py-2">Barcode</th><th class="border px-3 py-2">In or Out?</th><th class="border px-3 py-2">Destination</th><th class="border px-3 py-2">Airway Bill</th>
                </thead>
                <tbody class="">
                    <tr v-for="(dewar, index) in dewars" v-bind:key="index" class="hover:bg-blue-200">
                        <td class="p-2 border">{{dewar.date}}</td>
                        <td class="p-2 border">{{dewar.barcode.toUpperCase()}} <span v-if="dewar.sid"><a v-bind:href="'https://ispyb.diamond.ac.uk/shipments/sid/' + dewar.sid">&#8599;</a></span></td>
                        <td class="p-2 border">{{dewar.storageLocation.toUpperCase()}}</td>
                        <td class="p-2 border">{{dewar.destination}}</td>

                        <!-- If STORES OUT show links and/or plain AWB-->

                        <td v-if="dewar.storageLocation.toUpperCase() === 'STORES-OUT'">
                            <a class="text-blue-500"
                                v-if="isDHL(dewar.awb)"
                                v-on:mouseover="onGetCourierDestination(dewar)"
                                v-on:mouseleave="onResetCourierDestination(dewar)"
                                v-bind:href="'https://www.dhl.com/en/express/tracking.html?AWB=' + dewar.awb">{{dewar.awb}} (DHL)</a>
                            <a class="text-blue-500"
                                v-else-if="isFedexDatabaseRecord(dewar.awb)"
                                v-bind:href="'http://www.fedex.com/apps/fedextrack/?trackingnumber=' + dewar.awb">{{dewar.awb}} (FedEx)</a>
                            <span v-else>{{dewar.awb}}</span>
                            <div v-bind:class="[dewar.courierDestination ? 'absolute bg-gray-300 text-blue-400 p-px' : 'hidden']">
                                <p class="text-xl">DHL Destination: </p>
                                <p class="text-sm">{{dewar.courierDestination}}</p>
                            </div>
                        </td>

                        <!-- Else No value displayed if STORES-IN -->
                        <td v-else>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <footer class="py-4">
            <!-- Only here to provide some padding -->
        </footer>
  </div>
</template>

<script>
// Importing axios so we can cancel requests
import {Howl} from 'howler'

export default {
  name: 'stores',
    data() {
      return {
        // Array for dewar history
        dewars: [],
        // Data elements for form input
        barcode: '',
        location: '',
        awb: '',
        // Error message on find dewar, set location etc
        // isError if actual error, info otherwise
        message: "",
        isError: false,
        isFormOK: true,
        clearMessageInterval: 3, // Message interval in seconds
        refreshInterval: 3600, // Page Refresh interval in seconds (i.e. every hour)
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
    // Lifecycle hook - called when Vue is mounted on the page...
    mounted: function() {
        console.log("Vue App Instance Mounted")

        // When page is loaded set focus to the input location element
        this.$refs.location.focus();

        this.getDewars()
        // Set page to refresh every 60 minutes
        setInterval(this.refresh, this.refreshInterval * 1000)
    },
    watch: {
        message: function(val) {
            if (val !== "") {
                console.log("Clear message after " + this.clearMessageInterval + " s ")
                setTimeout(this.clearMessages, this.clearMessageInterval*1000)
            }
        }
    },
    methods: {
        refresh: function() {
            // window.localStorage.setItem('location', this.location)
            // We don't need to reload the page - just request an update from the server
            this.getDewars()
        },

        // Main method that retrieves dewar history from database
        getDewars: function() {
          let self = this
          self.dewars = []

          let url = this.$store.state.apiRoot + "stores/dewars"

          this.$http.get(url)
          .then(function(response) {
            console.log(response.data)
            let json = response.data
            let dewars = Object.keys(json);
            
            dewars.forEach(function(index) {
              let dewar = json[index]
              // Set a default courier destination so we can use it as popup later
              dewar.courierDestination = ''

              self.dewars.push(dewar)
            })
          })
          .catch(function() {
            console.log("Error getting initial data")
            self.message = "Error retrieving initial data"
            self.isError = true
          })
        },
        // Method to update dewar location in database
        onSetLocation: function(event) {
            console.log("onSetLocation")
            event.preventDefault()

            let self = this
            let validLocation = this.isValidLocation(this.location)

            if (this.barcode && this.location && validLocation) {
                let barcode = this.barcode
                let location = this.location
                let awb = ''
                // Only set Airway bill for Stores out
                if (location.toUpperCase() === "STORES-OUT") {
                    awb = this.awb // Field is optional

                    // If it's a Fedex code we want a 14 digit tracking number
                    if (this.isFedex(awb)) {
                        awb = this.getFedexTrackingNumber(awb)
                    }
                }

                let formData = new FormData();
                formData.append('barcode', barcode)
                formData.append('location', location)
                formData.append('awb', awb)

                let url = this.$store.state.apiRoot + "stores/dewars"
                
                this.$http.post(url, formData)
                .then(function(response) {
                    console.log(response)
                    let json = response.data
                    // Changed because we don't get the dewar id back from synchweb
                    // We get a DEWARHISTORYID instead
                    if ( json['DEWARHISTORYID'] > 0 ) {
                        self.message = "Updated " + barcode + " to " + location
                        self.isError = false
                        self.playSuccess()
                    } else {
                        self.message = "Error - no dewar history id returned"
                        self.isError = true
                        self.playFail();
                    }
                    // Request updated locations from DB                  
                    self.getDewars()
                })
                .catch(function(error) {
                    console.log(error)
                    self.message = "Error updating " + barcode + " to " + location
                    self.isError = true
                    self.playFail();
                })
                // Set focus to barcode (likely to want to reuse location)
                this.$refs.barcode.focus()
                // Rest form values (Keep location element as is)
                this.barcode = ''
                this.awb = ''    
            } else {
                this.message = "Issue with form: "
                this.isError = true
                if (this.barcode === "") {
                    this.message += " no barcode provided..."
                }
                if (this.location === "") {
                    this.message += ' no location provided...'
                } else if (!validLocation) {
                    this.message += ' location not valid for this application...'                            
                }
            }                 
        },

        // Reset Form fields
        onClearLocationForm: function(event) {
            event.preventDefault()          
            this.barcode = ''
            this.location = ''
            this.awb = ''
            // When form is cleared, set focus to the input location element
            this.$refs.location.focus();
        },
        // Get the intended courier destination
        // Currently only implemented for DHL but could be extended on backend
        onGetCourierDestination: function(dewar) {
            let url = this.$store.state.apiRoot + "stores/dewars/courier/destination"
            let theDewar = dewar
            // Set a flag on the dewar to indicate we are retrieving the courier destination
            theDewar.hover = true

            this.$http.get(url, {params: {'awb':dewar.awb}})
            .then(function(response) {
                // It's possible we have moved off the dewar link, in which case ignore the response
                if (theDewar.hover) {
                    let json = response.data
                    console.log(json)
                    theDewar.courierDestination = json.address.addressLocality
                }
            }).catch(function(error) {
                console.log(error)
            })
        },
        onResetCourierDestination: function(dewar) {
            // Its possible we have left before the api call returns.
            if (dewar.courierDestination) {
                dewar.courierDestination = ''
            }
            // Reset the "hover" tag
            dewar.hover = false
        },
        // Clear error/info messages in one go 
        clearMessages: function() {
          this.message = ""
          this.isError = false
        },
        // Internal validation method - check for DHL Airway Bill
        isDHL: function(awb) {
            let pattern1 = /^[0-9]{10}$/
            let pattern2 = /^JJ?D[0-9]{18}$/

            if (pattern1.test(awb) || pattern2.test(awb)) {
                return true
            } else {
                return false
            }
        },
        // Internal validation method - check for FedEx Airway Bill
        isFedex: function(awb) {
            // In future Fedex will only be 34 characters...
            // For now we need to accommodate 16 digits too
            let pattern1 = /^[0-9]{16}$/
            let pattern2 = /^[0-9]{34}$/

            if (pattern1.test(awb) || pattern2.test(awb)) {
                return true                        
            } else {
                return false
            }
        },
        // Validation method - used to determine value saved in ISPyB is Fedex
        isFedexDatabaseRecord: function(awb) {
            // In future we could check against delivery agent
            let pattern = /^[0-9]{14}$/

            if (pattern.test(awb)) {
                return true
            } else {
                return false
            }
        },
        // Method to return a tracking number for FedEx barcodes
        // New codes are 34 characters long but only the last 14 digits are the tracking number
        // Updated to handle legacy case where 16 digit code provided
        getFedexTrackingNumber: function(fedex_awb) {
            let result = fedex_awb

            if (fedex_awb.length === 16) {
                result = '00'+fedex_awb.slice(0,12)
            } else if (fedex_awb.length === 34) {
                result = fedex_awb.slice(-14)
            } else {
                console.log("Error - invalid fedex tracking code provided")
            }
            return result
        },
        // Internal validation method - check for valid location (stores in or out)
        isValidLocation: function(location) {
            if (location.toUpperCase() === "STORES-IN" || location.toUpperCase() === "STORES-OUT") {
                return true;
            } else {
                return false;
            }
        },

        // Prevent form submission and move focus to next form element
        onLocationEnter: function(event) {
            event.preventDefault()
            this.$refs.barcode.focus()
        },

        // Prevent form submission and move focus to next form element
        onBarcodeEnter: function(event) {
            event.preventDefault()

            if (this.isValidLocation(this.barcode)) {
                // Then user has entered barcode info here accidentally
                this.location = this.barcode
                this.barcode = ''
                this.$refs.barcode.focus()
            } else {
                if (this.location.toUpperCase() === 'STORES-IN') {
                    // In this case we submit the form
                    this.onSetLocation(event)
                } else {
                    this.$refs.awb.focus()
                }
            }
        },
        // Prevent form submission unless form conditions met
        onAwbEnter: function(event) {
            event.preventDefault()

            if (this.isValidLocation(this.awb)) {
                this.location = this.awb
                this.awb = ''
                this.$refs.barcode.focus()
            } else {
                if (this.barcode && this.location) {
                    // Try to submit form
                    this.onSetLocation(event)
                }
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


<!-- Small style changes to override default table colours -->
<style>
tr:nth-child(even) {
  @apply bg-blue-100;
}
</style>
