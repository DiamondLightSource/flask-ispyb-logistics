<!--
Card displaying container information stored in a specific rack location
-->
<template>
    <div class="border rounded shadow h-full p-2 cursor-pointer bg-blue-100 mb-2">
        <div v-if="container.code" class="flex justify-between">
            <span class="font-bold">{{container.code}}</span>
            <button class="text-xs mx-2 rounded p-2 items-end bg-red-500 hover:bg-red-600 text-white" @click="onRemoveFromBin(container.id)">Remove Container</button>
        </div>
        <span v-else class=""></span>
        <!-- Tags -->
        <div class="flex flex-col mb-2">
            <span v-if="container.arrivalDate" class="px-2 ">Arrival Date: {{container.arrivalDate.split(' ').slice(0,4).join(" ")}}</span>
            <span v-if="container.status" class="px-2 ">Status: {{container.status}}</span>
            <span v-if="container.id" class="px-2 ">ISPyB Link: <a class="underline" :href="'https://ispyb.diamond.ac.uk/containers/cid/'+container.id">{{container.id}}</a></span>
        </div>
    </div>
</template>


<script>
export default {
    name: 'ContainerCard',
    props: {
        container: Object,
    },
    methods: {
        onRemoveFromBin: function(id) {
            this.$emit('clear-container-from-bin', {id: id, location: this.container.location})
        },
    }
}
</script>