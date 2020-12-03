<template>
  <div>
    <div class="flex flex-col sm:flex-row">
      <div class="w-full md:w-1/3 border border-solid border-black m-2">
        <ScanContainer 
          v-bind:allowed_locations="allowed_locations"
          v-on:dewars-updated="handleDewarUpdate">
          </ScanContainer>
      </div>
      <div class="w-full md:w-1/3 border border-solid border-black m-2">
        <FindContainer></FindContainer>
      </div>
    </div>
    <!-- 
      Area for messages from back end 
      Currently conditional styling based on error or warning
    -->
    <MessagePanel></MessagePanel>
    
    <!-- Display the rack locations, four columns across If Zone 6 -->
    <div class="flex flex-wrap">
      <div class="w-full md:w-1/4 p-2" v-for="(dewar, rack) in rack_locations" v-bind:key="rack" v-on:click="onClearLocation(rack)">
        <ContainerCard 
          v-bind:container="dewar"
          v-bind:rack="rack">
        </ContainerCard>
      </div>
    </div>

    <!-- This pops up to confirm the clear location action -->
    <ClearLocationDialog 
      v-on:confirm-removal="onConfirmClear" 
      v-bind:isActive="isRemoveDialogActive"
      v-bind:locationToRemove="locationToRemove"
      v-bind:rack_locations="rack_locations">
    </ClearLocationDialog>
</template>

<script>
import ScanContainer from '@/components/ScanContainer.vue';
import FindContainer from '@/components/FindContainer.vue';
import DispatchDewars from '@/components/DispatchDewars.vue';
import MessagePanel from '@/components/MessagePanel.vue';
import ClearLocationDialog from '@/components/ClearLocationDialog.vue';
import ContainerCard from '@/components/ContainerCard.vue';

export default {
  name: 'Lab14Zone',

  components: {
    FindContainer,
    ScanContainer,
    DispatchDewars,
    MessagePanel,
    ClearLocationDialog,
    ContainerCard
  },
  data() {
    return {
      locationToRemove: null,
      isRemoveDialogActive: false,
      beamlines: [],

      rack_locations: {},
      // Timeout handle - used to determine if we need to refresh page
      refresh: null,
      refreshInterval: 60000, // refresh interval in milliseconds
    }
  },
  created: function() {
    // Get Valid Locations
    console.log("Lab14 Storage Zone Component Created")
    let self = this

    let url = this.$store.state.apiRoot + "beamlines/" + this.zone

    this.$http.get(url)
    .then(function(response) {
      let json = response.data
      self.beamlines = json
    })
    .catch(function(error) {
      console.log("Error getting valid beamline locations " + error)
    })
  },
  computed: {
    // We allow users to set the location for 'rack' and 'beamline' locations
      allowed_locations: function() {
        return this.beamlines.concat(Object.keys(this.rack_locations))
      },
      // Get the zone from the Vuex Store
      zone: function() {
        return this.$store.state.zone
      }
  },
  // Lifecycle hook - called when Vue is mounted on the page (trigger first get request)...
  mounted: function() {
    this.getContainers()
  },
  methods: {
    // Main method to retrieve dewar status for locations relevant to this zone
    getContainers: function() {
        let self = this
        let rack_data = {} // Placeholder for new data

        if (self.refresh) {
          // If we have been triggered by a form post/update,
          // Cancel the current timeout (avoid double refresh)
          clearTimeout(self.refresh)
        }

        let url = this.$store.state.apiRoot + "containers/locations/" + this.zone
    
        this.$http.get(url)
        .then(function(response) {
          let json = response.data

          let racklist = Object.keys(json)
          
          racklist.forEach(function(rack) {
            // Marshall the data into the format we want
            let dewarInfo = json[rack]
            let needsLN2 = false

            rack_data[rack] = {
              'barcode': dewarInfo.barcode,
              'arrivalDate': dewarInfo.arrivalDate,
              'facilityCode': '',
              'status': dewarInfo.status,
              'needsLN2': false,
              'onBeamline': false
            }
          })
          // Re-assign rack_locations property to trigger reactivity
          // Otherwise Vue has a hard time running computed properties
          self.rack_locations = rack_data
        })
        .catch(function(error) {
          let message = ""
          let isError = true
          if (error.response.status === 404) {
            // No dewars found - might be true
            message = "Warning no dewars found in these locations"

            // Set array to blank set so it shows placholders in page
            let racklist = Object.keys(error.response.data)
            
            console.log("Error but rack list = " + racklist)
            
            racklist.forEach(function(rack) {
              rack_data[rack] = {'barcode':'', 'arrivalDate':'', 'needsLN2': false, 'facilityCode': '', 'status': ''}
            })
            self.rack_locations = rack_data
          } else if (error.response.status == 503) {
            message = "ISPyB database service unavailable"
            console.log("Caught 503 Service unavailable...")
          } else {
            message = "Error retrieving dewar location information from database"
          }
          self.$store.commit('updateMessage', {text: message, isError: isError})
        })
        // Now setup the next update
        self.refresh = setTimeout(self.getBarcodes, self.refreshInterval)
      },
      
    // Handler for clear location event (rack location clicked)
    // This will trigger the confirm dialog box to show up
    onClearLocation: function(location) {
      console.log("on Clear Location clicked")
      // This location will be upper case because we control how it is rendered
      this.isRemoveDialogActive = true
      this.locationToRemove = location
    },
    // User has either confirmed or cancelled
    onConfirmClear: function(confirm) {
      if (confirm) {
        // Calling getBarodes straight away hits some cache issue
        // Delay the refresh so we ensure next call is accurate
        setTimeout(this.getBarcodes, 3000)
        // Brute force approach works if the timeout does not...
        // window.location.reload()
      }
      // Reset data that will disable dialog box
      this.locationToRemove = "";
      this.isRemoveDialogActive = false
    },
  }
}
</script>


<style>
.container-fluid {
  padding: 20px;
}

div.solid-border {
  border-style: solid;
  border-width: 1px 1px 1px 1px;
}

div.box {
  cursor: pointer;
}


</style>
