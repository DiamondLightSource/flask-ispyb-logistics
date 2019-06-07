<template>
  <div class="container-fluid">
    <div class="columns">
      <div class="column is-one-third solid-border">
        <ScanDewar 
          v-bind:allowed_locations="allowed_locations"
          v-on:dewars-updated="handleDewarUpdate">
          </ScanDewar>
      </div>
      <div class="column is-one-third solid-border">
        <FindDewar></FindDewar>
      </div>
      <div class="column is-one-third solid-border">
        <DispatchDewars v-bind:rack_locations="rack_locations"></DispatchDewars>
      </div>
    </div>

    <!-- 
      Area for messages from back end 
      Currently conditional styling based on error or warning
    -->
    <MessagePanel></MessagePanel>
    
    <!-- Display the rack locations, four columns across If Zone 6 -->
    <div v-if="zone==='zone6'" class=" solid-border columns is-multiline">
      <div class="column is-3" v-for="(dewar, rack) in rack_locations" v-bind:key="rack">
        <div class="box has-background-white-ter" v-on:click="onClearLocation(rack)" v-bind:class="{'has-text-danger': dewar.needsLN2 && dewar.status !== 'dispatch-requested'}">
          <span class="has-text-weight-bold">{{rack}}: </span>
          <span v-if="dewar.barcode" class="content has-text-weight-bold">{{dewar.barcode}}</span>
          <span v-else class="content is-invisible">empty</span>
          <!-- Tags -->
          <div class="tags has-addons">
            <span v-if="dewar.arrivalDate" class="tag is-info">{{dewar.arrivalDate.split(' ').slice(0,4).join(" ")}}</span>
            <span v-if="dewar.facilityCode" class="tag is-dark">{{dewar.facilityCode}}</span>
            <span v-if="dewar.status == 'dispatch-requested'" class="tag is-warning">{{dewar.status}}</span>
            <span v-else-if="dewar.needsLN2" class="tag is-danger">needs-refill</span>  
          </div>
        </div>
      </div>
    </div>

    <!-- Display the rack locations, six columns across If Zone 4 -->
    <div v-else-if="zone === 'zone4'" class=" solid-border columns is-multiline">
      <div class="column is-2" v-for="(dewar, rack) in rack_locations" v-bind:key="rack">
        <div class="box has-background-white-ter" v-on:click="onClearLocation(rack)" v-bind:class="{'has-text-danger': dewar.needsLN2 && dewar.status !== 'dispatch-requested'}">
          <span class="has-text-weight-bold">{{rack}}: </span>
          <span v-if="dewar.barcode" class="content has-text-weight-bold">{{dewar.barcode}}</span>
          <span v-else class="content is-invisible">empty</span>
          <!-- Tags -->
          <div class="tags has-addons">
            <span v-if="dewar.arrivalDate" class="tag is-info">{{dewar.arrivalDate.split(' ').slice(0,4).join(" ")}}</span>
            <span v-if="dewar.facilityCode" class="tag is-dark">{{dewar.facilityCode}}</span>
            <span v-if="dewar.status == 'dispatch-requested'" class="tag is-warning">{{dewar.status}}</span>
            <span v-else-if="dewar.needsLN2" class="tag is-danger">needs-refill</span>  
          </div>
        </div>
      </div>
    </div>

    <!-- Display the rack locations, four columns across If Zone 6 -->
    <div v-else-if="zone==='ebic'" class=" solid-border columns is-multiline">
      <div class="column is-3" v-for="(dewar, rack) in rack_locations" v-bind:key="rack">
        <div class="box has-background-white-ter" v-on:click="onClearLocation(rack)" v-bind:class="{'has-text-danger': dewar.needsLN2 && dewar.status !== 'dispatch-requested'}">
          <span class="has-text-weight-bold">{{rack}}: </span>
          <span v-if="dewar.barcode" class="content has-text-weight-bold">{{dewar.barcode}}</span>
          <span v-else class="content is-invisible">empty</span>
          <!-- Tags -->
          <div class="tags has-addons">
            <span v-if="dewar.arrivalDate" class="tag is-info">{{dewar.arrivalDate.split(' ').slice(0,4).join(" ")}}</span>
            <span v-if="dewar.facilityCode" class="tag is-dark">{{dewar.facilityCode}}</span>
            <span v-if="dewar.status == 'dispatch-requested'" class="tag is-warning">{{dewar.status}}</span>
            <span v-else-if="dewar.needsLN2" class="tag is-danger">needs-refill</span>  
          </div>
        </div>
      </div>
    </div>

    <!-- Default display if unknown location requested -->
    <div v-else>
      <p>No known storage location</p>
    </div>

    <!-- This pops up to confirm the clear location action -->
    <ClearLocationDialog 
      v-on:confirm-removal="onConfirmClear" 
      v-bind:isActive="isRemoveDialogActive"
      v-bind:locationToRemove="locationToRemove"
      v-bind:rack_locations="rack_locations">
    </ClearLocationDialog>
  </div>

</template>

<script>
import ScanDewar from '@/components/ScanDewar.vue';
import FindDewar from '@/components/FindDewar.vue';
import DispatchDewars from '@/components/DispatchDewars.vue';
import MessagePanel from '@/components/MessagePanel.vue';
import ClearLocationDialog from '@/components/ClearLocationDialog.vue';

export default {
  name: 'DewarZone',
  props: ['zone'],

  components: {
    FindDewar,
    ScanDewar,
    DispatchDewars,
    MessagePanel,
    ClearLocationDialog
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
    console.log("Dewar Storage Zone Component Created")
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
  },
  // Lifecycle hook - called when Vue is mounted on the page (trigger first get request)...
  mounted: function() {
      this.getBarcodes()
  },
  methods: {
      handleDewarUpdate: function() {
        console.log("Dewar updated OK")
        this.getBarcodes()
      },
      // Main method to retrieve dewar status for locations relevant to this zone
      getBarcodes: function() {
          let self = this
          let rack_data = {} // Placeholder for new data

          if (self.refresh) {
            // If we have been triggered by a form post/update,
            // Cancel the current timeout (avoid double refresh)
            clearTimeout(self.refresh)
          }

          let url = this.$store.state.apiRoot + "dewars/locations/" + this.zone
      
          this.$http.get(url)
          .then(function(response) {
            let json = response.data

            let racklist = Object.keys(json)
            
            racklist.forEach(function(rack) {
              let barcode = json[rack][0]
              let arrivalDate = json[rack][1]
              let facilityCode = json[rack][2]
              let status = json[rack][3]
              let needsLN2 = false

              // Check here if arrivalData > 5 days    
              if (arrivalDate !== "") {
                let nowSecs = new Date().getTime()/1000;
                let lastFillSeconds = Date.parse(arrivalDate)/1000

                let deltaTime = nowSecs - lastFillSeconds

                if (deltaTime > 5*24*3600) {
                  needsLN2 = true
                }
              }
              rack_data[rack] = {'barcode': barcode, 'arrivalDate': arrivalDate, 'needsLN2': needsLN2, 'facilityCode': facilityCode, 'status': status}
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
          // This location will be upper case because we control how it is rendered
          this.isRemoveDialogActive = true
          this.locationToRemove = location
        },
        // User has either confirmed or cancelled
        onConfirmClear: function(confirm) {
          if (confirm) {
            // Force a refresh of the data
            this.getBarcodes()
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

</style>
