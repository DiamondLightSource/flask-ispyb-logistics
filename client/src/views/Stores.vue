<template>
  <div class="stores">
        <div class="container-fluid">

            <!-- First set of columns are the top form elements -->
            <div class="columns">

                <!-- Form element to set locations -->
                <div class="column is-half solid-border">
                    <h2 class="title has-text-centered">Scan Dewar and Barcode</h2>

                    <form>
                        <div class="field">
                            <label>Location</label>
                            <div class="control">
                            <input ref="location" type="text" class="input" v-model="location" v-on:keydown.enter="onLocationEnter" placeholder="Scan the location e.g. STORES-IN or STORES-OUT">        
                            </div>
                        </div>

                        <div class="field">
                            <label>Barcode</label>
                            <div class="control">
                                <input ref="barcode" type="text" class="input" v-model="barcode" v-on:keydown.enter="onBarcodeEnter" placeholder="Scan the QR code / barcode from the dewar case">
                            </div>
                        </div>

                        <!-- If location is STORES-IN do not show AWB field...-->
                        <div v-show="location.toUpperCase() != 'STORES-IN'" class="field">
                            <label>Airway Bill</label>
                            <div class="control">
                                <input ref="awb" type="text" class="input" v-model="awb" v-on:keydown.enter="onAwbEnter" placeholder="Scan the DHL / FedEx Airway Bill">
                            </div>
                        </div>
                    
                        <div class="columns">
                            <div class="column">
                                <button type="submit" class="button is-link is-fullwidth" v-on:click="onSetLocation">Submit</button>              
                            </div>
                            <div class="column">
                                <button type="cancel" class="button is-info is-fullwidth"  v-on:click="onClearLocationForm">Cancel</button>
                            </div>
                        </div>        
                    </form>

                </div>


                <div class="column is-half solid-border"> <!-- STORES LOCATIONS  -->
                    <h2 class="title has-text-centered">Locations</h2>
                    <br />
                    <nav class="level">
                        <div class="level-item has-text-centered">
                            <div>
                                <img width=96 src='../assets/img/stores-in.gif'>
                                <p class="subtitle">STORES-IN</p>                
                            </div>
                        </div>
                        <div class="level-item has-text-centered">
                            <div>
                                <img width=96 src='../assets/img/stores-out.gif'>
                                <p class="subtitle">STORES-OUT</p>
                            </div>
                        </div>
                    </nav>   
                </div> <!-- END STORES LOCATIONS -->


            </div> <!-- End of columns -->

            <!-- 
                Area for messages from back end 
                Currently conditional render based on error or warning
            -->
            <div v-if="message" class="columns">
                <article class="column is-12 message" v-bind:class="[isError ? 'is-danger' : 'is-info']">
                    <div class="message-body subtitle">
                    {{message}}
                    </div>
                </article>
            </div>

        </div> <!-- END container fluid -->

        <!-- Display the stores history -->
        <div class="container-fluid">
            <div class="has-text-centered">
                <h1 class="title">History</h1>
            </div>            
            <br />
            <table class="table is-bordered is-fullwidth is-striped">
                <thead class="center-table">
                    <th>Date/Time</th><th>Barcode</th><th>In or Out?</th><th>Destination</th><th>Airway Bill</th>
                </thead>
                <tbody class="center-table">
                    <tr v-for="(dewar, index) in dewars" v-bind:key="index">
                        <td>{{dewar.date}}</td>
                        <td>{{dewar.barcode.toUpperCase()}} <span v-if="dewar.sid"><a v-bind:href="'https://ispyb.diamond.ac.uk/shipments/sid/' + dewar.sid">&#8599;</a></span></td>
                        <td>{{dewar.inout.toUpperCase()}}</td>
                        <td>{{dewar.destination}}</td>
                        <!-- If STORES OUT show links and/or plain AWB-->
                        <td v-if="dewar.inout.toUpperCase() === 'STORES-OUT'">
                            <a v-if="isDHL(dewar.awb)" v-bind:href="'http://www.dhl.com/en/express/tracking.html?AWB=' + dewar.awb">{{dewar.awb}}</a>
                            <a v-else-if="isFedexDatabaseRecord(dewar.awb)" v-bind:href="'http://www.fedex.com/apps/fedextrack/?trackingnumber=' + dewar.awb">{{dewar.awb}}</a>
                            <span v-else>{{dewar.awb}}</span>
                        </td>
                        <!-- Else No value displayed if STORES-IN -->
                        <td v-else>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
  </div>
</template>

<script>
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
        refreshInterval: 30 // 3600, // Page Refresh interval in seconds (i.e. every hour)
      }
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
    methods: {
        refresh: function() {
            console.log('Refresh - saving location in localStorage')
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
                        // self.playSuccess()
                    } else {
                        self.message = "Error - no dewar history id returned"
                        self.isError = true
                        // self.playFail();
                    }
                    // Request updated locations from DB                  
                    self.getDewars()
                })
                .catch(function(error) {
                    console.log(error)
                    self.message = "Error updating " + barcode + " to " + location
                    self.isError = true
                    // self.playFail();
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
    }
}
</script>


<!-- Small style changes to override default bulma css -->
<style>
  .container-fluid {
    padding: 20px;
  }

  div.solid-border {
    border-style: solid;
    border-width: 1px 1px 1px 1px;
  }

  .center-table th {
      text-align: center;
      vertical-align: middle;
  }
  
  .center-table td {
      text-align: center;
      vertical-align: middle;
  }

</style>