<template>
  <div class="bg-gray-200">
    <div class="flex flex-col sm:flex-row">
      <div class="w-full md:w-1/3 border border-solid border-black m-2">
        <FindContainer></FindContainer>
      </div>
      <div class="w-full md:w-1/3 border border-solid border-black m-2">
        <ScanContainer 
          v-bind:allowed_locations="allowed_locations"
          v-on:dewars-updated="refreshContainers">
          </ScanContainer>
      </div>
    </div>
    <!-- 
      Area for messages from back end 
      Currently conditional styling based on error or warning
    -->
    <MessagePanel></MessagePanel>
    
    <!-- Display the rack locations, four columns across If Zone 6 -->
    <!-- Lab 14 Needs three columns of locations ULT, RF, RT -->
    <div class="flex flex-wrap mt-4 border-t border-solid border-black">
      <div class="w-1/3">
        <storage-location
          title="Storage Location: ULT"
          :locations="ult_locations"
          @remove-container-from-bin="onRemoveContainerFromBin"
          @clear-containers="onClearAllContainersFromBin"
        />
      </div>
      <div class="w-1/3">
        <storage-location
          title="Storage Location: RF"
          :locations="rf_locations"
          @remove-container-from-bin="onRemoveContainerFromBin"
          @clear-containers="onClearAllContainersFromBin"
        />
      </div>
      <div class="w-1/3">
        <storage-location
          title="Storage Location: RT"
          :locations="rt_locations"
          @remove-container-from-bin="onRemoveContainerFromBin"
          @clear-containers="onClearAllContainersFromBin"
        />
      </div>
    </div>

    <!-- This pops up to confirm the clear location action -->
    <ClearContainerDialog 
      v-on:confirm-removal="onConfirmClear" 
      v-bind:isActive="isRemoveDialogActive"
      v-bind:locationToRemove="locationToRemove"
      v-bind:containerId="containerId"
      v-bind:beamlines="beamlines">
    </ClearContainerDialog>
  </div>
</template>

<script>
import ScanContainer from '@/components/ScanContainer.vue';
import FindContainer from '@/components/FindContainer.vue';
import MessagePanel from '@/components/MessagePanel.vue';
import ClearContainerDialog from '@/components/ClearContainerDialog.vue';
import StorageLocation from '@/components/StorageLocation.vue';

export default {
  name: 'Lab14Zone',

  components: {
    FindContainer,
    ScanContainer,
    MessagePanel,
    ClearContainerDialog,
    'storage-location': StorageLocation,
  },
  data() {
    return {
      containerId: 0,
      isRemoveDialogActive: false,
      locationToRemove: '',
      beamlines: [],

      rack_locations: {},
      container_data: [],
      // Timeout handle - used to determine if we need to refresh page
      refresh: null,
      refreshInterval: 60000, // refresh interval in milliseconds
      message: '',
      container_locations: [],
    }
  },
  created: function() {
    // Get Valid Locations
    this.getBeamlineLocations()
  },
  computed: {
    // We allow users to set the location for 'rack' and 'beamline' locations
      allowed_locations: function() {
        return this.beamlines.concat(this.container_locations.map( function(item) { return item.location }))
      },
      // Get the zone from the Vuex Store
      zone: function() {
        return this.$store.state.zone
      },
      ult_locations: function() {
        // Group all 'ult' locations into an array
        let ult = this.container_locations.filter( function(item) {
          return item.location.toLowerCase().startsWith('ult')
        })
        return ult
      },
      rf_locations: function() {
        let filtered = this.container_locations.filter( function(item) {
          return item.location.toLowerCase().startsWith('rf')
        })
        return filtered
      },
      rt_locations: function() {
        let filtered = this.container_locations.filter( function(item) {
          return item.location.toLowerCase().startsWith('rt')
        })
        return filtered
      }
  },
  // Lifecycle hook - called when Vue is mounted on the page (trigger first get request)...
  mounted: function() {
    this.getContainers()
  },
  methods: {
    refreshContainers: function() {
      // Control updating cards with container info
      if (this.refresh) clearTimeout(this.refresh)
      this.getContainers()
      // Now setup the next update
      this.refresh = setTimeout(this.getContainers, this.refreshInterval)
    },
    getBeamlineLocations: function() {
      let self = this
      let url = this.$store.state.apiRoot + "beamlines/" + this.zone

      this.$http.get(url)
      .then(function(response) {
        self.beamlines = response.data.map( (bl) => bl.toLowerCase())
      })
      .catch(function(error) {
        console.log("Error getting valid beamline locations " + error)
      })
    },
    // Main method to retrieve container status for locations relevant to this zone
    getContainers: function() {
      let self = this
      // let rack_data = {}
      let data = []
      let url = this.$store.state.apiRoot + "containers/locations/" + this.zone
  
      this.$http.get(url).then(function(response) {
        data = self.handleContainersOK(response.data)
      })
      .catch(function(error) {
        data = self.handleContainersFailed(error)
      }).finally( function() {
        self.setLocationContents(data)
      })
    },

    handleContainersOK: function(payload) {
      // let racklist = Object.keys(payload)
      let container_locations = []
      
      payload.forEach(function(item) {
        // Info should be an array of items
        container_locations.push(item)
      })
      return container_locations
    },

    handleContainersFailed: function(error) {
      let message = this.getErrorMessage(error.response.status)
      
      this.$store.dispatch('updateMessage', {text: message, isError: true})
      
      return error.response.data
    },

    getErrorMessage: function(status) {
      if (status === 404) return "No containers found in these locations"
      else if (status == 503) return "ISPyB database service unavailable"
      else return "Error retrieving container information from database"
    },
    setLocationContents: function(data) {
        // Triggers vue reactivity so computed properties work
        this.container_locations = data.filter( function() { return true })    
    },
    onClearAllContainersFromBin: function(ids) {
      ids.forEach( function(id) {
        console.log("Clear containers from bin " + id)
      })
    },
    onRemoveContainerFromBin: function(payload) {
      console.log("Remove Container From Bin " + payload.id)
      this.isRemoveDialogActive = true
      this.containerId = payload.id
      this.locationToRemove = payload.location
    },    
    // User has either confirmed or cancelled
    onConfirmClear: function(confirm) {
      if (confirm) {
        // Calling getBarodes straight away hits some cache issue
        // Delay the refresh so we ensure next call is accurate
        setTimeout(this.getContainers, 3000)
        // Brute force approach works if the timeout does not...
        // window.location.reload()
      }
      // Reset data that will disable dialog box
      this.containerId = 0;
      this.isRemoveDialogActive = false
      this.locationToRemove = ''
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
