<template>
  <div class="home">
    <div class="container">
        <!-- Title Section-->
        <div class="hero">
            <div class="hero-body has-text-centered">
                <div class="container">
                    <h1 class="title">
                        ISPyB Logistics Applications
                    </h1>
                    <h2 class="subtitle">
                        These applications help track dewars at specific locations in the facility.
                    </h2>
                </div>
            </div>
        </div>

        <!-- Layout for application links -->
        <div class="columns">
            <div class="column is-one-quarter">
                <a href="/stores/">
                    <div class="box notification is-success">
                        <p class="title">Stores Dewar Management</p>
                        <p class="content">To handle dewars coming into or out of the facility</p>
                    </div>
                </a>
            </div>

            <div class="column is-one-quarter">
                <a href="/zone6/">
                    <div class="box notification is-success">
                        <p class="title">Zone 6 Dewar Management</p>
                        <p class="content">To handle dewars to and from beamlines</p>
                    </div>
                </a>
            </div>

            <div class="column is-one-quarter">
                <a href="/zone4/">
                    <div class="box notification is-success">
                        <p class="title">Zone 4 Dewar Management</p>
                        <p class="content">To handle dewars in the WES storage unit</p>
                    </div>
                </a>
            </div>

            <div class="column is-one-quarter">
                <a href="/ebic/">
                    <div class="box notification is-success">
                        <p class="title">eBIC Dewar Management</p>
                        <p class="content">To handle dewars to and from eBIC</p>
                    </div>
                </a>
            </div>
        </div>
      </div>
      <!-- Footer with link to scisoft -->
      <footer class="footer has-text-centered">For questions about these applications, please contact Scientific Software <a href="mailto:scientificsoftware@diamond.ac.uk?Subject=ISPyBLogistics">here</a></footer>
    </div> <!-- END of main container -->
</template>

<script>
export default {
  name: 'home',
}
</script>

<style>

div.solid-border {
  border-style: solid;
  border-width: 1px 1px 1px 1px;
}

div.box {
  cursor: pointer;
}


</style>
