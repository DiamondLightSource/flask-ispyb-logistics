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
            <h1 class="text-xl">Dewar Report</h1>
            </header>
        <section class="p-4">
          <p class="mb-2">Enter report information for dewar {{barcode}}</p>
          <form>
              <ul class="flex flex-col">
                <li class="flex"><label class="w-1/3 px-2">Hard drive present?</label><input v-model="hddPresent" type="checkbox" /></li>
                <li class="flex"><label class="w-1/3 px-2">Tools present?</label><input v-model="toolsPresent" type="checkbox" /></li>
                <li class="flex"><label class="w-1/3 px-2">T bar missing?</label><input v-model="tBarMissing" type="checkbox" /></li>
                <li class="flex"><label class="w-1/3 px-2">Vent damaged?</label><input v-model="ventDamaged" type="checkbox" /></li>
                <li class="flex"><label class="w-1/3 px-2">Foam plug missing?</label><input v-model="foamPlugMissing" type="checkbox" /></li>
                <li class="flex"><label class="w-1/3 px-2">Dewar warm?</label><input v-model="dewarWarm" type="checkbox" /></li>
                <li class="flex mt-2"><label class="w-1/3 px-2">Comments: </label><textarea v-model="comments" class="w-2/3 border border-gray-500 rounded leading-tight p-2" /></li>
              </ul>
          </form>
        </section>
        <footer class="flex border-t-2 justify-end">
          <button class="text-white bg-success hover:bg-green-700 rounded p-1 m-2" v-on:click="onSave()">Save</button>
          <button class="text-white bg-danger hover:bg-red-700 rounded p-1 m-2" v-on:click="onClose()">Cancel</button>
        </footer>
      </div>
    </div>

</template>

<script>

function initialState() {
    return {
        hddPresent: false,
        toolsPresent: false,
        tBarMissing: false,
        ventDamaged: false,
        foamPlugMissing: false,
        dewarWarm: false,
        comments: ''
    }
}

export default {
    name: 'DewarReportDialog',
    props: ['isActive', 'barcode'],
    data() {
        return initialState()
    },
    methods: {
        // User has confirmed to remove the dewar from this location
        onSave: function() {
            var report = []
            report.push("---")
            report.push("hdd: " + this.hddPresent)
            report.push("tools: " + this.toolsPresent)
            report.push("tbar: " + this.tBarMissing)
            report.push("vent: " + this.ventDamaged)
            report.push("foamPlug: " + this.foamPlugMissing)
            report.push("warm: " + this.dewarWarm)
            report.push("comments: " + this.comments)
            report.push("---")

            var output = report.join('\n')
            console.log(output)

            Object.assign(this.$data, initialState())

            this.$emit("confirm-update", true)
        },
        // User has cancelled        
        onClose: function() {
            Object.assign(this.$data, initialState())
            this.$emit("confirm-update", false)
        }
    }
}
</script>