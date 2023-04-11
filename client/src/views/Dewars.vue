<template>
  <div class="">
    <div class="flex flex-col sm:flex-row">
      <div class="w-full md:w-1/3 border border-solid border-black m-2">
        <ScanDewar 
          v-bind:allowed_locations="allowed_locations"
          v-on:dewars-updated="handleDewarUpdate">
          </ScanDewar>
      </div>
      <div class="w-full md:w-1/3 border border-solid border-black m-2">
        <FindDewar></FindDewar>
      </div>
      <div class="w-full md:w-1/3 border border-solid border-black m-2">
        <DispatchDewars v-bind:rack_locations="rack_locations"></DispatchDewars>
      </div>
    </div>

    <!-- 
      Area for messages from back end 
      Currently conditional styling based on error or warning
    -->
    <MessagePanel></MessagePanel>
    
    <!-- Display the rack locations, four columns across If Zone 6 -->
    <div v-if="zone==='zone6'" class="flex flex-wrap">
      <div class="w-full md:w-1/4 p-2" v-for="(dewar, rack) in rack_locations" v-bind:key="rack">
        <DewarCard
          v-on:update-dewar="onShowDewarReport"
          v-bind:dewar="dewar"
          v-bind:rack="rack">
        </DewarCard>
      </div>
    </div>

    <!-- Display the rack locations, six columns across If Zone 4 -->
    <div v-else-if="zone === 'zone4'" class="flex flex-wrap">
      <div class="w-full md:w-1/6 p-2" v-for="(dewar, rack) in rack_locations" v-bind:key="rack" >
        <DewarCard
          v-on:update-dewar="onShowDewarReport"
          v-bind:dewar="dewar"
          v-bind:rack="rack">
        </DewarCard>
      </div>
    </div>

    <!-- Display the rack locations, four columns across If Zone 6 -->
    <div v-else-if="zone==='ebic'" class="flex flex-wrap">
      <div class="w-full md:w-1/4 p-2" v-for="(dewar, rack) in rack_locations" v-bind:key="rack">
        <DewarCard 
          v-on:update-dewar="onShowDewarReport"
          v-bind:dewar="dewar"
          v-bind:rack="rack">
        </DewarCard>
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
      v-bind:barcodeToRemove="barcodeToRemove"
      v-bind:rack_locations="rack_locations">
    </ClearLocationDialog>

    <DewarReportDialog
      v-bind:isActive="dewarId !== 0"
      v-bind:dewarId="dewarId"
      v-bind:dewarBarcode="dewarBarcode"
      v-bind:dewarComments="dewarComments"
      v-bind:dewarContainers="dewarContainers"
      v-on:confirm-update="onConfirmUpdateDewarReport"
      v-on:clear-location="onClearLocation">
    </DewarReportDialog>

  </div>

</template>

<script>
import ScanDewar from '@/components/ScanDewar.vue';
import FindDewar from '@/components/FindDewar.vue';
import DispatchDewars from '@/components/DispatchDewars.vue';
import MessagePanel from '@/components/MessagePanel.vue';
import ClearLocationDialog from '@/components/ClearLocationDialog.vue';
import DewarReportDialog from '@/components/DewarReportDialog.vue';
import DewarCard from '@/components/DewarCard.vue';

export default {
  name: 'DewarZone',

  components: {
    FindDewar,
    ScanDewar,
    DispatchDewars,
    MessagePanel,
    ClearLocationDialog,
    DewarCard,
    DewarReportDialog
  },
  data() {
    return {
      barcodeToRemove: null,
      isRemoveDialogActive: false,
      beamlines: [],

      rack_locations: {},
      // Timeout handle - used to determine if we need to refresh page
      refresh: null,
      refreshInterval: 60000, // refresh interval in milliseconds
      // Dewar Report id
      dewarId: 0,
      dewarBarcode: '',
      dewarComments: '',
      dewarContainers: '',
    }
  },
  created: function() {
    // Get Valid Locations
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
      this.getBarcodes()
  },
  methods: {
      handleDewarUpdate: function() {
        this.getBarcodes()
      },
      // Main method to retrieve dewar status for locations relevant to this zone
      getBarcodes: function() {
          let self = this

          if (self.refresh) {
            // If we have been triggered by a form post/update,
            // Cancel the current timeout (avoid double refresh)
            clearTimeout(self.refresh)
          }

          let url = this.$store.state.apiRoot + "dewars/locations/" + this.zone
      
          this.$http.get(url).then(function(response) {
            // Re-assign rack_locations property to trigger reactivity
            // Otherwise Vue has a hard time running computed properties
            self.rack_locations = self.handleUpdateBarcodesOK(response)
          })
          .catch(function(error) {
            self.rack_locations = self.handleUpdateBarcodesError(error)
          })
          // Now setup the next update
          self.refresh = setTimeout(self.getBarcodes, self.refreshInterval)
        },

        handleUpdateBarcodesOK: function(response) {
          let json = response.data
          let rack_data = {} // Placeholder for new data

          let racklist = Object.keys(json)
          
          racklist.forEach(function(rack) {
            // Marshall the data into the format we want
            let dewarInfo = json[rack]
            let needsLN2 = false
            // Flag to indicate dewar is on beamline (and therefore space is taken)...
            let onBeamline = dewarInfo.onBeamline ? dewarInfo.onBeamline : false

            // Check here if topup > 5 days ago (and dewar is not on beamline being processed)
            if (dewarInfo.arrivalDate !== "" && !onBeamline) {
              let nowSecs = new Date().getTime()/1000;
              let lastFillSeconds = 0;
              // Topups are now recorded in the comments field
              if ('comments' in dewarInfo && dewarInfo.comments != null) {
                let dewarComments = JSON.parse(dewarInfo.comments)
                if ('toppedUp' in dewarComments) {
                  lastFillSeconds = Date.parse(dewarComments.toppedUp.slice(-1)[0])/1000
                }
              }

              let deltaTime = nowSecs - lastFillSeconds

              if (deltaTime > 5*24*60*60) {
                needsLN2 = true
              }
            }

            rack_data[rack] = {
              'dewarId': dewarInfo.dewarId,
              'comments': dewarInfo.comments,
              'dewarContainers': dewarInfo.dewarContainers,
              'barcode': dewarInfo.barcode,
              'arrivalDate': dewarInfo.arrivalDate,
              'facilityCode': dewarInfo.facilityCode,
              'status': dewarInfo.status,
              'needsLN2': needsLN2,
              'onBeamline': onBeamline
            }
          })

          // Return rack data
          return rack_data
        },
        handleUpdateBarcodesError: function(error) {
            let message = ""
            let isError = true
            let rack_data = {} // Placeholder for new data

            if (error.response.status === 404) {
              // No dewars found - might be true
              message = "Warning no dewars found in these locations"

              // Set array to blank set so it shows placholders in page
              let racklist = Object.keys(error.response.data)
                            
              racklist.forEach(function(rack) {
                rack_data[rack] = {'barcode':'', 'arrivalDate':'', 'needsLN2': false, 'facilityCode': '', 'status': ''}
              })
            } else if (error.response.status == 503) {
              message = "ISPyB database service unavailable"
              console.log("Caught 503 Service unavailable...")
            } else {
              message = "Error retrieving dewar location information from database"
            }
            this.$store.dispatch('updateMessage', {text: message, isError: isError})

            return rack_data
        },
        // Handler for clear location event (rack location clicked)
        // This will trigger the confirm dialog box to show up
        onClearLocation: function(barcode) {
          // This location will be upper case because we control how it is rendered
          this.isRemoveDialogActive = true
          this.barcodeToRemove = barcode
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
          this.barcodeToRemove = "";
          this.isRemoveDialogActive = false
        },
        // Handler for clear location event (rack location clicked)
        // This will trigger the confirm dialog box to show up
        onShowDewarReport: function(dewar) {
          // This location will be upper case because we control how it is rendered
          this.dewarComments = dewar.comments
          this.dewarId = dewar.dewarId
          this.dewarBarcode = dewar.barcode
          this.dewarContainers = dewar.dewarContainers
        },
        // User has either confirmed or cancelled
        onConfirmUpdateDewarReport: function(payload) {
          if (payload.status) {
            this.updateDewarReport(payload.dewarId, payload.report)
          }
          // Reset data that will disable dialog box
          this.dewarId = 0;
          this.dewarComments = '';
          this.dewarBarcode = '';
          this.dewarContainers = '';
        },
        updateDewarReport: function(dewarId, comments) {
          let url = this.$store.state.apiRoot + "dewars/comments/" + dewarId
          
          let formData = new FormData();
          formData.append('comments', comments)

          this.$http.patch(url, formData).then( () => {
            this.$store.dispatch('updateMessage', {text: 'Comments Updated OK', isError: false})
            // Trigger a refresh so we see the new comments
            setTimeout(this.getBarcodes, 3000)
          }).catch( () => {
            this.$store.dispatch('updateMessage', {text: 'Error updating dewar comments', isError: true})
          })
        }
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
