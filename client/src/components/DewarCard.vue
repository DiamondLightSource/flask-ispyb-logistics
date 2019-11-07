<!--
Card displaying dewar information stored in a specific rack location

Emits an event 'clear-location' which should be handled by the parent component
-->
<template>
    <div class="border rounded shadow h-full p-4 cursor-pointer"
        v-bind:class="{'text-danger': dewar.needsLN2 && dewar.status !== 'dispatch-requested', 'bg-gray-400' : dewar.onBeamline}">
        <span class="font-bold">{{rack}}: </span>
        <span v-if="dewar.barcode" class="font-bold">{{dewar.barcode}}</span>
        <span v-else class=""></span>
        <!-- Tags -->
        <div class="flex flex-wrap">
            <span v-if="dewar.arrivalDate" class="text-xs text-white bg-info py-1 px-2 ">{{dewar.arrivalDate.split(' ').slice(0,4).join(" ")}}</span>
            <span v-if="dewar.facilityCode" class="text-xs text-white bg-gray-900 py-1 px-2">{{dewar.facilityCode}}</span>
            <span v-if="dewar.status == 'dispatch-requested'" class="text-xs bg-warning py-1 px-2 ">{{dewar.status}}</span>
            <span v-else-if="dewar.needsLN2" class="text-xs text-white bg-danger py-1 px-2 ">needs-refill</span>  
        </div>
    </div>
</template>


<script>
export default {
    name: 'DewarCard',
    props: {
        dewar: Object,
        rack: String
    },
}
</script>