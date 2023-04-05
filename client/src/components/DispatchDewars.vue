<template>
    <section>
        <transition name="fade" mode="out-in">
            <section v-if="show_refill && page == 1" key="1">
                <h2 class="text-3xl text-center font-bold py-2">Dewars that need refilling</h2>
                <ul>
                    <li v-for="(dewar, index) in refill_dewars.slice(0, 5)" v-bind:key="index">
                        <p class="px-2 text-lg text-center text-black bg-danger mx-4"><b>{{dewar}}</b></p>
                    </li>
                </ul>
                <footer class="">
                    <div class="text-center py-2">
                        <p>(Scan dewars with location LN2TOPUP after refilling)</p>
                    </div>
                </footer>
            </section>
            <section v-else-if="show_refill && page == 2" key="2">
                <h2 class="text-3xl text-center font-bold py-2">Dewars that need refilling</h2>
                <ul>
                    <li v-for="(dewar, index) in refill_dewars.slice(5, 10)" v-bind:key="index">
                        <p class="px-2 text-lg text-center text-black bg-danger mx-4"><b>{{dewar}}</b></p>
                    </li>
                </ul>
                <footer class="">
                    <div class="text-center py-2">
                        <p>(Scan dewars with location LN2TOPUP after refilling)</p>
                    </div>
                </footer>
            </section>
            <section v-else-if="show_refill && page == 3" key="3">
                <h2 class="text-3xl text-center font-bold py-2">Dewars that need refilling</h2>
                <ul>
                    <li v-for="(dewar, index) in refill_dewars.slice(10, 15)" v-bind:key="index">
                        <p class="px-2 text-lg text-center text-black bg-danger mx-4"><b>{{dewar}}</b></p>
                    </li>
                </ul>
                <footer class="">
                    <div class="text-center py-2">
                        <p>(Scan dewars with location LN2TOPUP after refilling)</p>
                    </div>
                </footer>
            </section>
            <section v-else-if="show_refill && page == 4" key="4">
                <h2 class="text-3xl text-center font-bold py-2">Dewars that need refilling</h2>
                <ul>
                    <li v-for="(dewar, index) in refill_dewars.slice(15, 20)" v-bind:key="index">
                        <p class="px-2 text-lg text-center text-black bg-danger mx-4"><b>{{dewar}}</b></p>
                    </li>
                </ul>
                <footer class="">
                    <div class="text-center py-2">
                        <p>(Scan dewars with location LN2TOPUP after refilling)</p>
                    </div>
                </footer>
            </section>
            <section v-else-if="show_dispatch && page == 1" key="5">
                <h2 class="text-3xl text-center font-bold py-2">Dewars that need dispatching</h2>
                <ul>
                    <li v-for="(dewar, index) in dispatch_dewars.slice(0, 5)" v-bind:key="index">
                        <p class="px-2 text-lg text-center text-black bg-warning mx-4"><b>{{dewar}}</b></p>
                    </li>
                </ul>
                <footer class="">
                    <div class="text-center py-2">
                        <p>(Scan dewars to Stores when removed from rack)</p>
                    </div>
                </footer>
            </section>
            <section v-else-if="show_dispatch && page == 2" key="6">
                <h2 class="text-3xl text-center font-bold py-2">Dewars that need dispatching</h2>
                <ul>
                    <li v-for="(dewar, index) in dispatch_dewars.slice(5, 10)" v-bind:key="index">
                        <p class="px-2 text-lg text-center text-black bg-warning mx-4"><b>{{dewar}}</b></p>
                    </li>
                </ul>
                <footer class="">
                    <div class="text-center py-2">
                        <p>(Scan dewars to Stores when removed from rack)</p>
                    </div>
                </footer>
            </section>
            <section v-else-if="show_dispatch && page == 3" key="7">
                <h2 class="text-3xl text-center font-bold py-2">Dewars that need dispatching</h2>
                <ul>
                    <li v-for="(dewar, index) in dispatch_dewars.slice(10, 15)" v-bind:key="index">
                        <p class="px-2 text-lg text-center text-black bg-warning mx-4"><b>{{dewar}}</b></p>
                    </li>
                </ul>
                <footer class="">
                    <div class="text-center py-2">
                        <p>(Scan dewars to Stores when removed from rack)</p>
                    </div>
                </footer>
            </section>
            <section v-else-if="show_dispatch && page == 4" key="8">
                <h2 class="text-3xl text-center font-bold py-2">Dewars that need dispatching</h2>
                <ul>
                    <li v-for="(dewar, index) in dispatch_dewars.slice(15, 20)" v-bind:key="index">
                        <p class="px-2 text-lg text-center text-black bg-warning mx-4"><b>{{dewar}}</b></p>
                    </li>
                </ul>
                <footer class="">
                    <div class="text-center py-2">
                        <p>(Scan dewars to Stores when removed from rack)</p>
                    </div>
                </footer>
            </section>
        </transition>
    </section>
</template>

<script>
export default {
    name: 'DispatchDewars',
    props: {
        rack_locations: Object
    },
    data() {
      return {
          show_refill: true,
          show_dispatch: false,
          page: 1
      }
    },  
    computed: {
        // This is used to display 5 dewars that need refilling
        // If they have dispatch requested show them anyway - SCI-10162
        refill_dewars: function() {
            const self = this
            let dewars = Object.keys(this.rack_locations).filter( function(rack) {
                return self.rack_locations[rack].needsLN2 === true
            })
            return dewars
        },

        // This is used to display 5 dewars that need to be dispatched
        dispatch_dewars: function() {
            const self = this
            let dewars = Object.keys(this.rack_locations).filter( function(rack) {
                return self.rack_locations[rack].status === 'dispatch-requested'
            })
            return dewars
        }
    },
    methods: {
        cycleDispatchDewarView: function() {
            if (this.show_refill) {
                if (this.refill_dewars.length<this.page*5 || this.page == 4) {
                    this.show_refill = false
                    this.show_dispatch = true
                    this.page = 1
                } else {
                    this.page = this.page+1
                }
            } else {
                if (this.dispatch_dewars.length<this.page*5 || this.page == 4) {
                    this.show_dispatch = false
                    this.show_refill = true
                    this.page = 1
                } else {
                    this.page = this.page+1
                }
            }
        }
    },
    mounted: function() {
        setInterval(this.cycleDispatchDewarView, 5000)
    }
}
</script>

<style>
/* CSS to control transition event */
.fade-enter-active, .fade-leave-active {
  transition: opacity .5s
}
.fade-enter, .fade-leave-to {
  opacity: 0
}
</style>
