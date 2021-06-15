<!--
Storage Bin displaying container information stored in a specific location
-->
<template>
    <div class="border border-solid border-gray-500 rounded shadow h-full p-4 cursor-pointer bg-gray-100">
			<div class="flex justify-between">
				<h2 class="font-bold">Storage Bin: {{title}}</h2>
				<button class="mb-2 p-1 rounded text-white bg-red-500 hover:bg-red-600" @click.prevent="onClearBin">Clear Bin</button>
			</div>

			<div class="flex flex-col m-1" v-for="container in containers" v-bind:key="container.id">
				<ContainerCard
					:container="container"
					v-on="$listeners"/>
			</div>
    </div>
</template>


<script>
import ContainerCard from '@/components/ContainerCard.vue';
export default {
    name: 'StorageBin',
    props: {
        title: String,
				containers: {
					type: Array,
					default: function() { return [] }
				}
    },
		components: {
			ContainerCard,
		},
		methods: {
			onClearBin: function() {
				let filtered = this.containers.filter( item => item.id != '')
				let containerIds = filtered.map( function(item) { 
					if (item.id != '') return item.id
				})
				if (containerIds) this.$emit('clear-containers', {containers: containerIds, storageBin: this.title})
			},
		}
}
</script>