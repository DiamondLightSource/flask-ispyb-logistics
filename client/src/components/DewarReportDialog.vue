<!--
Modal Dialog Box to confirm removal of a dewar from a location

Emits an event 'confirm-removal' with a boolean true/false if user confirmed action
-->
<template>
    <!-- This pops up to confirm the clear location action -->
    <div v-if="isActive" 
        class="fixed inset-0 w-full h-screen flex items-center justify-center bg-semi-75"
        v-on:click.self="onClose()">
        <button
            aria-label="close"
            class="absolute top-0 right-0 text-xl text-gray-500 font-bold my-2 mx-4" 
            @click.prevent="onClose()">x</button>
      <div class="w-1/2 bg-white shadow-lg rounded-lg p-4">
        <header class="border-b-2">
            <h1 class="text-xl">Dewar Report for dewar {{ dewarBarcode }}</h1>
            </header>
        <section class="p-4">
              <ul class="flex flex-col">
                <li class="flex mt-2"><label class="w-1/3 px-2">Containers in dewar: </label>
                  <span v-html="formattedContainers" class="w-2/3 leading-tight pb-2"></span>
                </li>
              </ul>
          <form>
              <ul class="flex flex-col">
                <li class="flex" v-if="visit">
                  <label class="w-1/3 px-2">Visit</label>
                  <span class="w-2/3 leading-tight pb-2">{{ visit + ' - ' + beamline + ' - ' + startDateString }}</span>
                </li>
                <li class="flex"><label class="w-1/3 px-2">Hard drive present?</label><input v-model="hdd" type="checkbox" /></li>
                <li class="flex"><label class="w-1/3 px-2">Tools present?</label><input v-model="tools" type="checkbox" /></li>
                <li class="flex"><label class="w-1/3 px-2">T bar missing?</label><input v-model="tBarMissing" type="checkbox" /></li>
                <li class="flex"><label class="w-1/3 px-2">Vent damaged?</label><input v-model="ventDamaged" type="checkbox" /></li>
                <li class="flex"><label class="w-1/3 px-2">Foam plug missing?</label><input v-model="foamPlugMissing" type="checkbox" /></li>
                <li class="flex"><label class="w-1/3 px-2">Dewar warm?</label><input v-model="dewarWarm" type="checkbox" /></li>
                <li class="flex"><label class="w-1/3 px-2">LN2 topups</label><input v-model="toppedUp" type="text" class="w-2/3 leading-tight py-2" readonly/></li>
                <li class="flex"><label class="w-1/3 px-2">Dewar checked?</label><input v-model="checked" type="text" class="w-2/3 leading-tight py-2" readonly/></li>
                <li class="flex mt-2"><label class="w-1/3 px-2">Comments: </label><textarea v-model="comments" class="w-2/3 border border-gray-500 rounded leading-tight p-2" /></li>
              </ul>
          </form>
        </section>
        <footer class="flex border-t-2 justify-between">
          <div>
            <button class="text-white bg-success hover:bg-green-700 rounded px-2 py-1 m-2" v-on:click="onSave()"><i class="fa fa-check pr-2"></i>Save Report</button>
            <button class="text-white bg-danger hover:bg-red-700 rounded px-2 py-1 m-2" v-on:click="onClose()"><i class="fa fa-times pr-2"></i>Cancel</button>
          </div>
          <button class="text-white bg-blue-500 hover:bg-blue-700 rounded px-2 py-1 m-2" v-on:click.prevent="viewInSynchweb(shippingId)"><i class="fa fa-link pr-2"></i>View in Synchweb</button>
          <button class="text-white bg-red-700 hover:bg-red-900 rounded px-2 py-1 m-2" v-on:click.prevent="clearLocation(dewarBarcode)"><i class="fa fa-trash pr-2"></i>Clear Dewar</button>
        </footer>
      </div>
    </div>

</template>

<script>
// Dewar.comments is tinytext = 255 characters
const MAX_CONTENT_LENGTH = 255

function initialState() {
    return {
        hdd: false,
        tools: false,
        tBarMissing: false,
        ventDamaged: false,
        foamPlugMissing: false,
        dewarWarm: false,
        toppedUp: "",
        checked: "",
        comments: "",
    }
}

export default {
    name: 'DewarReportDialog',
    emits: ['confirm-update', 'clear-location'],
    props: {
        isActive: {
            type: Boolean,
            default: false,
        },
        dewarBarcode: {
            type: String,
        },
        dewarId: {
            type: Number,
            required: true,
        },
        shippingId: {
            type: Number,
        },
        dewarComments: {
            type: String,
        },
        dewarContainers: {
            type: String,
        },
        visit: {
            type: String,
        },
        beamline: {
            type: String,
        },
        startDate: {
            type: String,
        },
        startDateString: {
            type: String,
        },
    },
    data() {
        return initialState()
    },
    watch: {
        dewarComments: function(newVal) {
            if (newVal) this.initialiseReport(newVal)
        },
    },
    computed: {
        formattedContainers: function() {
            if (Array.isArray(this.dewarContainers)) {
                return this.dewarContainers.join("<br />");
            }
            return this.dewarContainers || '';
        }
    },
    methods: {
        // To conserve characters save each boolean as 1 or 0
        initialiseReport: function(comments) {
            let json;
            try {
                json = JSON.parse(comments)
            } catch (err) {
                json = comments
                console.log("data already in json format.")
            }
            try {
                this.hdd = parseInt(json.hdd) === 1,
                this.tools = parseInt(json.tools) === 1,
                this.tBarMissing = parseInt(json.tBarMissing) === 1,
                this.ventDamaged = parseInt(json.ventDamaged) === 1,
                this.foamPlugMissing = parseInt(json.foamPlugMissing) === 1,
                this.dewarWarm = parseInt(json.warm) === 1,
                this.toppedUp = json.toppedUp || "",
                this.checked = json.checked || "",
                this.comments = json.comments || ""
            } catch (err) {
                console.log("Error passed comments that had data in but were null: " + comments)
            }
        },
        // User has confirmed to remove the dewar from this location
        onSave: function() {
            let content = this.buildReportAsJSON()

            let result = this.checkLengthValid(content)

            if (result == false) this.$store.dispatch('updateMessage', {text: 'Error report is too long, must be < 256 characters', isError: true})

            this.$emit('confirm-update', {dewarId: this.dewarId, report: content, status: result})
    
            Object.assign(this.$data, initialState())
        },
        // User has cancelled        
        onClose: function() {
            Object.assign(this.$data, initialState())
            this.$emit('confirm-update', {status: false})
        },
        // Build a json format report
        buildReportAsJSON: function() {
            let report = {}

            report['hdd'] = this.hdd ? 1 : 0
            report['tools'] = this.tools ? 1 : 0
            report['tBarMissing'] = this.tBarMissing ? 1 : 0
            report['ventDamaged'] = this.ventDamaged ? 1 : 0
            report['foamPlugMissing'] = this.foamPlugMissing ? 1 : 0
            report['warm'] = this.dewarWarm ? 1 : 0

            if (this.toppedUp) report['toppedUp'] = this.toppedUp
            if (this.checked) report['checked'] = this.checked

            if (this.comments) report['comments'] = this.comments

            return JSON.stringify(report)
        },
        checkLengthValid: function(comments) {
            console.log("Comments length = " + comments.length)
            return comments.length > MAX_CONTENT_LENGTH ? false : true
        },
        clearLocation: function(barcode) {
            this.onClose()
            console.log("Clear Dewar " + barcode)
            this.$emit('clear-location', barcode)
        },
        viewInSynchweb: function(shippingId) {
            console.log("Opening Synchweb link to " + shippingId)
            let url = "https://ispyb.diamond.ac.uk/shipments/sid/" + shippingId
            window.open(url, '_blank').focus();
        },
    }
}
</script>
