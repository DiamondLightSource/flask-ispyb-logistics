<template>
    <div class="container mx-auto">
        <!-- Title Section-->
        <div class="flex">
            <div class="w-full text-center mt-4">
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
            <div class="m-2 p-4">
                <a href="/stores/" class="">
                    <div class="text-center bg-green-500 p-4 rounded h-full">
                        <p class="text-white text-2xl font-bold">Stores Dewar Management</p>
                        <p class="">To handle dewars coming into or out of the facility</p>
                    </div>
                </a>
            </div>

            <div class="m-2 p-4">
                <a href="/zone6/" class="">
                    <div class="text-center bg-green-500 p-4 rounded h-full">
                        <p class="text-white text-2xl font-bold">Zone 6 Dewar Management</p>
                        <p class="">To handle dewars to and from beamlines</p>
                    </div>
                </a>
            </div>

            <div class="m-2 p-4">
                <a href="/zone4/" class="">
                    <div class="text-center bg-green-500 p-4 rounded h-full">
                        <p class="text-white text-2xl font-bold">Zone 4 Dewar Management</p>
                        <p class="">To handle dewars in the WES storage unit</p>
                    </div>
                </a>
            </div>

            <div class="m-2 p-4">
                <a href="/ebic/" class="">
                    <div class="text-center bg-green-500 p-4 rounded h-full">
                        <p class="text-white text-2xl font-bold">eBIC Dewar Management</p>
                        <p class="">To handle dewars to and from eBIC</p>
                    </div>
                </a>
            </div>
        </div>
      <!-- Footer with link to scisoft -->
      <footer class="text-center">For questions about these applications, please contact Scientific Software <a href="mailto:scientificsoftware@diamond.ac.uk?Subject=ISPyBLogistics">here</a></footer>
    </div> <!-- END of main container -->
</template>

<script>
export default {
  name: 'home',
}
</script>

<style>

</style>
