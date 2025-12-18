<template>
    <section>
        <h2 class="text-3xl text-center font-bold py-2">Find a Dewar</h2>
        <form>
          <div class="mb-3 px-2">
            <label class="block text-gray-700">BarCode or FacilityCode</label>
            <input type="text" class="shadow appearance-none border rounded w-full py-1 px-3 text-gray-700 leading-tight focus:outline-none focus:ring" v-model="facilitycode" placeholder="e.g. DLS-MX-####">
          </div>
          <div class="flex">
            <button type="submit" class="text-white bg-link hover:bg-blue-800 rounded p-1 m-2 w-1/2" v-on:click="onFindDewar">Search</button>            
            <button type="submit" class="text-white bg-info hover:bg-blue-600 rounded p-1 m-2 w-1/2" v-on:click="onClearFindForm">Cancel</button>            
          </div>
          <div v-if="searchResult" class="flex flex-col text-left">
              <p class="text-xl p-4">Location History</p>
              <ul class="timeline">
                <li v-for="(item, index) in searchResult.slice(0,5)" v-bind:key="index" class="timeline-container">
                  <div class="timeline-content">
                      <p>{{ item.location }}</p>
                      <!-- Arrival Date uses filter defined in this component -->
                      <p class="tag">{{ format_date(item.arrivalDate) }}</p>
                  </div>
                </li>
              </ul>
          </div>
          <div v-else-if="searchResultError" class="flex text-left">
              <p class="text-xl px-4 text-danger">{{ searchResultError }}</p>
          </div>
        </form>
    </section>
</template>

<script>
import axios from 'axios'

export default {
    name: 'FindDewar',

    data() {
        return {
            searchResult: null,
            searchResultError: null,
            facilitycode: '',
        }
    },
    watch: {
        searchResult: function(newValue) {
            // Close after 5 seconds
            if (newValue) {
                setTimeout(this.clearMessages, 10000);
            }
        },
    },
    methods: {
        format_date: function(value) {
            if (!value) 
                return ''
            let d = new Date(value)
            return d.toUTCString()
        },
        // Search the database for a dewar with the specified facility code (DLS-MX-1234)
        // Some values in the history can be null so we need to handle those
        onFindDewar: function(event) {
            event.preventDefault()
            console.log("Find Dewar")

            if (this.facilitycode !== "") {
                let self = this
                let facilitycode = this.facilitycode
                // Get API Root from store
                let url = this.$store.state.apiRoot + "dewars/find"

                axios.get(url, {params: {'fc':facilitycode}})
                .then(function(response) {
                    let json = response.data

                    // Changed location to an array of objects to show recent history...
                    // Should be array of {location: 'storageLocation', arrivalDate: 'arrival date'}
                    let locations = json["storageLocations"]

                    // Convert locations to uppercase if we have a value (handle null entries)
                    locations.forEach(function(item) {
                        item.location = item.location ? item.location.toUpperCase() : "none"
                    })
                    self.searchResult = locations
                })
                .catch(function() {
                    self.searchResult = null
                    self.searchResultError = "Dewar " + facilitycode + " not found"
                })
                .finally(function() {
                    // Clear up after query - could reset facility code input here?
                    //self.facilitycode = ''
                })
            } else {
                // This provides feedback message in main error/info area
                this.message = "No facility code provided"
            }
        },
        onClearFindForm: function(event) {
            event.preventDefault()    
            this.facilitycode = ''
        },
        // Clear all messages in one go 
        clearMessages: function() {
            this.searchResult = null
            this.searchResultError = null
        },
    }
}
</script>
<style>
/* Timeline css see https://www.w3schools.com/howto/howto_css_timeline.asp */
.timeline {
    position: relative;
    margin: 10px;
}
/* This draws the line */
.timeline::after {
    content: "";
    position: absolute;
    top: 5px;
    bottom: 5px;
    left: 10px;
    margin-left: 0px;
    width: 4px;
    background-color: grey;
}
/* Position each block of content */
.timeline-container {
    position: relative;
    margin-left: 40px;
    padding: 10px;
}
/* Make the first entry stand out (most recent item) */
.timeline-container:first-child {
    font-weight: bold;
    color: red;
}
/* The circles on the timeline */
.timeline-container::after {
    content: '';
    position: absolute;
    width: 25px;
    height: 25px;
    left: -40px;
    top: 10px;
    background-color: white;
    border: 4px solid grey;
    border-radius: 50%;
    z-index: 1;
}
.timeline-container:first-child::after {
    background-color: red;
}
.timeline-content {
    font-size: 1.2em;
}
</style>
