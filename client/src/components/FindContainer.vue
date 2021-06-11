<template>
    <section>
        <h2 class="text-3xl text-center font-bold py-2">Check Container</h2>
        <form>
          <div class="mb-3 px-2">
            <label class="block text-gray-700">BarCode</label>
            <input type="text" class="shadow appearance-none border rounded w-full py-1 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" v-model="barcode" placeholder="e.g. cm1234-b21-1234">
          </div>
          <div class="flex">
            <button type="submit" class="text-white bg-link hover:bg-blue-800 rounded p-1 m-2 w-1/2" v-on:click.prevent="onFindContainer">Search</button>
            <button type="submit" class="text-white bg-info hover:bg-blue-600 rounded p-1 m-2 w-1/2" v-on:click.prevent="onClearForm">Cancel</button>
          </div>
          <div v-if="searchResult" class="flex flex-col text-left">
              <p class="text-xl font-bold px-2">ContainerInformation</p>
              <p class="text-md px-2">Shipment: {{searchResult.shipmentName}}</p>
              <p class="text-md px-2">Location: {{searchResult.location}}</p>
              <p class="text-md px-2">Storage Temperature: {{searchResult.temperature}}</p>
          </div>
          <div v-else-if="searchResultError" class="flex text-left">
              <p class="text-xl px-4 text-danger">{{ searchResultError }}</p>
          </div>
        </form>
    </section>
</template>

<script>

export default {
    name: 'FindContainer',

    data() {
        return {
            searchResult: null,
            searchResultError: null,
            barcode: '',
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
    filters: {
        format_date: function (value) {
            if (!value) return ''

            let d = new Date(value)
        
            return d.toUTCString()
        }
    },
    methods: {
        // Search backend for recent location of this container
        onFindContainer: function() {
            if (this.barcode) this.findContainer(this.barcode)
            else setErrorMessage("No facility code provided")
        },
        onClearForm: function() {
            this.barcode = ''
            this.searchResultError = null
        },
        // Clear all messages in one go 
        clearMessages: function() {
            this.searchResult = null
            this.searchResultError = null
        },
        findContainer: function() {
            // Get API Root from store
            let url = this.$store.state.apiRoot + "containers/find"

            this.$http.get(url, {params: {'barcode': this.barcode}})
            .then( this.containerFound )
            .catch( this.containerNotFound )
        },
        setErrorMessage: function(message) {
            this.searchResultError = message
        },
        containerFound: function(response) {
            let json = response.data
            // Changed location to an array of objects to show recent history...
            // Should be array of {location: 'location', arrivalDate: 'arrival date'}
            let storageTemperature = json["storageTemperature"]
            let shippingName = json["shippingName"]
            let location = json["location"]

            this.searchResult = {temperature: storageTemperature, shipmentName: shippingName, location: location}
        },
        containerNotFound: function() {
            this.searchResult = null
            this.searchResultError = "Container not found"            
        }
    }
}
</script>