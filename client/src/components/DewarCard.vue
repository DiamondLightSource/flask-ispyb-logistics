<!--
Card displaying dewar information stored in a specific rack location

Emits an event 'clear-location' which should be handled by the parent component
-->
<template>
    <div class="border rounded shadow h-full p-4 cursor-pointer relative split"
        v-on:click.prevent="showDewarReport(dewar)"
        :class="[
            dewar.dewarId && !dewar.onBeamline ? 'split-' + dewar.daysSinceTopup : '',
            dewar.needsLN2 && dewar.status !== 'dispatch-requested' ? 'text-danger' : '',
            dewar.onBeamline ? 'bg-gray-400' : ''
        ]"
    >
        <span class="font-bold">{{rack}}: </span>
        <span v-if="dewar.barcode" class="font-bold">{{dewar.barcode}}</span>
        <span v-else class=""></span>
        <!-- Tags -->
        <div class="flex flex-wrap">
            <span v-if="dewar.arrivalDate" class="text-xs text-white bg-info py-1 px-2 ">{{dewar.arrivalDate.split(' ').slice(0,4).join(" ")}}</span>
            <span v-if="dewar.facilityCode" class="text-xs text-white bg-gray-900 py-1 px-2">{{dewar.facilityCode}}</span>
            <span v-if="dewar.status == 'dispatch-requested'" class="text-xs bg-warning py-1 px-2 ">{{dewar.status}}</span>
            <span v-if="dewar.needsLN2" class="text-xs text-white bg-danger py-1 px-2 ">needs-refill</span>
            <span v-if="dewar.beamline" class="text-xs text-white bg-success py-1 px-2 ">{{dewar.beamline}}</span>
            <span v-if="dewar.UDC" class="text-xs text-white bg-primary py-1 px-2 ">UDC</span>
        </div>
    </div>
</template>


<script>
export default {
    name: 'DewarCard',
    emits: ['update-dewar'],
    props: {
        dewar: Object,
        rack: String
    },
    methods: {
        showDewarReport: function(dewar) {
            if (dewar.startDate) {
                dewar.startDateString = new Date(dewar.startDate).toLocaleString("en-GB", {weekday:"short", month:"short", day:"numeric", hour:"numeric", minute:"numeric"})
            }
            if (dewar.dewarId) {
                console.log("Update Dewar from " + dewar.dewarId)
                this.$emit('update-dewar', dewar)
            }
        }
    }
}
</script>

<style>
.split::before {
  content: "";
  position: absolute;
  top: 0;
  right: 0;
  width: 4px;                     /* thickness */
  height: 100%;
  border-radius: inherit;
}

.split-0::before {
  background: linear-gradient(
    to bottom,
    blue 0%,
    blue 100%
  );
}

.split-1::before {
  background: linear-gradient(
    to bottom,
    red 0%,
    red 20%,
    blue 20%,
    blue 100%
  );
}

.split-2::before {
  background: linear-gradient(
    to bottom,
    red 0%,
    red 40%,
    blue 40%,
    blue 100%
  );
}

.split-3::before {
  background: linear-gradient(
    to bottom,
    red 0%,
    red 60%,
    blue 60%,
    blue 100%
  );
}

.split-4::before {
  background: linear-gradient(
    to bottom,
    red 0%,
    red 80%,
    blue 80%,
    blue 100%
  );
}

.split-5::before {
  background: linear-gradient(
    to bottom,
    red 0%,
    red 100%
  );
}
</style>
