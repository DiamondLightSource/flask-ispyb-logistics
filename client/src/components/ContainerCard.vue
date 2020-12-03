<!--
Card displaying container information stored in a specific rack location
-->
<template>
    <div class="border rounded shadow h-full p-4 cursor-pointer"
        v-bind:class="{'text-danger': container.needsLN2 && container.status !== 'dispatch-requested', 'bg-gray-400' : container.onBeamline}">
        <span class="font-bold">{{rack}}: </span>
        <span v-if="container.barcode" class="font-bold">{{container.barcode}}</span>
        <span v-else class=""></span>
        <!-- Tags -->
        <div class="flex flex-wrap">
            <span v-if="container.arrivalDate" class="text-xs text-white bg-info py-1 px-2 ">{{container.arrivalDate.split(' ').slice(0,4).join(" ")}}</span>
            <span v-if="container.facilityCode" class="text-xs text-white bg-gray-900 py-1 px-2">{{container.facilityCode}}</span>
            <span v-if="container.status == 'dispatch-requested'" class="text-xs bg-warning py-1 px-2 ">{{container.status}}</span>
            <span v-else-if="container.needsLN2" class="text-xs text-white bg-danger py-1 px-2 ">needs-refill</span>
        </div>
    </div>
</template>


<script>
export default {
    name: 'ContainerCard',
    props: {
        container: Object,
        rack: String
    },
}
</script>