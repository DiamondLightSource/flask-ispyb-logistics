<template>
	<!-- Displays a list of storage bins -->
	<div class="m-4">
		<h1 class="text-center text-lg font-bold mb-2">{{title}}</h1>
		<div v-for="bin in bins" :key="bin.location" class="mb-4">
			<storage-bin
				:title="bin.location"
				:containers="bin.containers"
				@clear-containers="onShowClearStorageBin"
				@clear-container-from-bin="onShowClearContainer"
			/>
		</div>

		<!-- This pops up to confirm the clear all bins within a storage location -->
		<clear-storage-bin-dialog 
      v-on:confirm-removal="onConfirmClearStorageBin" 
      v-bind:isActive="isClearStorageBinActive"
      v-bind:storageBin="storageBin"
      v-bind:containers="containersToRemove">
		</clear-storage-bin-dialog>

    <!-- This pops up to confirm the clear location action -->
    <clear-container-dialog 
      v-on:confirm-removal="onConfirmClearContainer" 
      v-bind:isActive="isClearContainerActive"
      v-bind:locationToRemove="locationToRemove"
      v-bind:containerId="containerId">
    </clear-container-dialog>
	</div>
</template>

<script>
import StorageBin from '@/components/StorageBin.vue'
import ClearStorageBinDialog from '@/components/ClearStorageBinDialog.vue';
import ClearContainerDialog from '../components/ClearContainerDialog.vue';

export default {
	name: 'storage-location',
	props: {
		title: String,
		locations: {
			type: Array,
			default: function() { return [] }
		}
	},
	components: {
		'storage-bin': StorageBin,
    'clear-container-dialog': ClearContainerDialog,
		'clear-storage-bin-dialog': ClearStorageBinDialog
	},
	data() {
		return {
			isClearStorageBinActive: false,
			containersToRemove: [],
			storageBin: '',
			// Attributes needed to clear container from location
      isClearContainerActive: false,
      containerId: 0,
      locationToRemove: '',
		}
	},
	computed: {
		// We need to group the data based on common bin location ULT-1, ULT-2 etc.
		bins: function() {
			let result = []
			let keys = []
			this.locations.filter( function(item) {
				if (keys.indexOf(item.location) > -1) return false
				else {
					keys.push(item.location)
					return true
				}
			}, keys)

			// For each key, create the bins
			let self = this
			keys.forEach( function(key) {
				let bin = self.locations.filter( function(item) {
					if (item.location == key) return true
				}, key, result )

				result.push( {location: key, containers: bin[0].containers})
			})
			return result
		}
	},
	methods: {
		onShowClearStorageBin: function(payload) {
			// This trick reliably triggers the vue reactivity
			this.containersToRemove = payload.containers.filter( () => { return true })
			this.storageBin = payload.storageBin
			this.isClearStorageBinActive = true
    },
		// User has either confirmed or cancelled
    onConfirmClearStorageBin: function(confirm) {
      if (confirm) this.$emit('storage-location-changed')
      // Reset data that will disable dialog box
      this.containersToRemove = [];
			this.storageBin = ''
      this.isClearStorageBinActive = false
    },
		onShowClearContainer: function(payload) {
			if (!payload.id || !payload.location) {
				this.$store.dispatch('updateMessage', {text: 'Error with payload from clear-container event', isError: true})
				return
			}
      this.isClearContainerActive = true
      this.containerId = payload.id
      this.locationToRemove = payload.location
    },    
    // User has either confirmed or cancelled
    onConfirmClearContainer: function(confirm) {
      if (confirm) this.$emit('storage-location-changed')
      // Reset data that will disable dialog box
      this.containerId = 0;
      this.isClearContainerActive = false
      this.locationToRemove = ''
    },
	}
}
</script>

ContainerBin