<template>
    <div class="container mx-auto">
        <!-- Title Section-->
        <div class="flex">
            <div class="w-full text-center py-8 px-4">
                <h1 class="text-4xl font-bold">
                    ISPyB Logistics Applications
                </h1>
                <h2 class="text-xl">
                    These applications help track dewars at specific locations in the facility.
                </h2>
            </div>
        </div>
    
        <!-- Layout for application links -->
        <div class="flex flex-col md:flex-row">
            <div class="p-4" v-if="showStores == 1">
                <a href="/stores/" class="">
                    <div class="text-white text-center bg-success p-4 rounded h-full">
                        <p class="text-3xl font-bold">Stores Dewar Management</p>
                        <p class="">To handle dewars coming into or out of the facility</p>
                    </div>
                </a>
            </div>

            <div class="p-4" v-if="showZone6 == 1">
                <a href="/zone6/" class="">
                    <div class="text-white text-center bg-success p-4 rounded h-full">
                        <p class="text-3xl font-bold">Zone 6 Dewar Management</p>
                        <p class="">To handle dewars to and from beamlines</p>
                    </div>
                </a>
            </div>

            <div class="p-4" v-if="showZone4 == 1">
                <a href="/zone4/" class="">
                    <div class="text-white text-center bg-success p-4 rounded h-full">
                        <p class="text-3xl font-bold">Zone 4 Dewar Management</p>
                        <p class="">To handle dewars in the WES storage unit</p>
                    </div>
                </a>
            </div>

            <div class="p-4" v-if="showEBIC == 1">
                <a href="/ebic/" class="">
                    <div class="text-white text-center bg-success p-4 rounded h-full">
                        <p class="text-3xl font-bold">eBIC Dewar Management</p>
                        <p class="">To handle dewars to and from eBIC</p>
                    </div>
                </a>
            </div>
            <div class="p-4" v-if="showLab14 == 1">
                <a href="/lab14/" class="">
                    <div class="text-white text-center bg-success p-4 rounded h-full">
                        <p class="text-3xl font-bold">Lab14 Container Management</p>
                        <p class="">To handle containers for SCM</p>
                    </div>
                </a>
            </div>
            <div class="p-4" v-if="showCage == 1">
                <a href="/cage/" class="">
                    <div class="text-white text-center bg-success p-4 rounded h-full">
                        <p class="text-3xl font-bold">SLS Dewar Management</p>
                        <p class="">To handle dewar trolleys for SLS</p>
                    </div>
                </a>
            </div>
            <div class="p-4" v-if="showI19 == 1">
                <a href="/i19/" class="">
                    <div class="text-white text-center bg-success p-4 rounded h-full">
                        <p class="text-3xl font-bold">I19 Dewar Management</p>
                        <p class="">To handle dewars for I19</p>
                    </div>
                </a>
            </div>
        </div>
      <!-- Footer with link to scisoft -->
      <footer class="text-center">For questions about these applications, please contact Scientific Software <a class="text-blue-500 underline" href="mailto:scientificsoftware@diamond.ac.uk?Subject=ISPyBLogistics">here</a></footer>
    </div> <!-- END of main container -->
</template>

<script>
import { envFlag } from '@/env'

export default {
  name: 'home',
  data() {
    return {
      showStores: import.meta.env?.VITE_SHOW_STORES || process.env.VUE_APP_SHOW_STORES,
      showZone4:  import.meta.env?.VITE_SHOW_ZONE4  || process.env.VUE_APP_SHOW_ZONE4,
      showZone6:  import.meta.env?.VITE_SHOW_ZONE6  || process.env.VUE_APP_SHOW_ZONE6,
      showLab14:  import.meta.env?.VITE_SHOW_LAB14  || process.env.VUE_APP_SHOW_LAB14,
      showEBIC:   import.meta.env?.VITE_SHOW_EBIC   || process.env.VUE_APP_SHOW_EBIC,
      showCage:   import.meta.env?.VITE_SHOW_CAGE   || process.env.VUE_APP_SHOW_CAGE,
      showI19:    import.meta.env?.VITE_SHOW_I19    || process.env.VUE_APP_SHOW_I19,
    }
  }
}
</script>

<style>

</style>
