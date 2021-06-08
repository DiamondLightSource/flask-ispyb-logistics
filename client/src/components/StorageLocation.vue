<template>
	<!-- Displays a list of storage bins -->
	<div class="m-4">
		<h1 class="text-center text-lg font-bold mb-2">{{title}}</h1>
		<div v-for="bin in bins" :key="bin.location" class="mb-4">
			<storage-bin
				:title="bin.location"
				:containers="bin.containers"
				v-on="$listeners"
			/>
		</div>
	</div>
</template>

<script>
import StorageBin from '@/components/StorageBin.vue'

export default {
	name: 'storage-location',
	props: {
		title: String,
		locations: {
			type: Array,
			default: function() { return [] }
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
	components: {
		'storage-bin': StorageBin,
	},
}
</script>

ContainerBin