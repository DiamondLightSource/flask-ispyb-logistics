<template>
    <section>
        <transition name="fade" mode="out-in">
            <section v-if="show_dewars" key="1">
                <h2 class="title has-text-centered">Dewars that need refilling</h2>
                <ul>
                <li v-for="(dewar, index) in refill_dewars.slice(0, 5)" v-bind:key="index">
                    <p class="is-size-5 has-text-centered has-background-danger has-text-black"><b>{{dewar}}</b></p>
                </li>
                </ul>
                <footer class="footer has-background-white-ter is-paddingless">
                <div class="content has-text-centered">
                    <p>(Scan dewars back into the same position after refilling)</p>
                </div>
                </footer>
            </section>
            <section v-else key="2">
            <h2 class="title has-text-centered">Dewars that need dispatching</h2>
            <ul>
                <li v-for="(dewar, index) in dispatch_dewars.slice(0, 5)" v-bind:key="index">
                <p class="is-size-5 has-text-centered has-background-warning has-text-black"><b>{{dewar}}</b></p>
                </li>
            </ul>
            <footer class="footer has-background-white-ter is-paddingless">
                <div class="content has-text-centered">
                <p>(Dewars in need of dispatch - clear once removed from rack)</p>
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
          show_dewars: true
      }
    },  
    computed: {
        // This is used to display 5 dewars that need refilling
        // If they have dispatch requested set ignore them (they are leaving the facility so don't need LN2)
        refill_dewars: function() {
            const self = this
            let dewars = Object.keys(this.rack_locations).filter( function(rack) {
                return self.rack_locations[rack].status !== 'dispatch-requested' && self.rack_locations[rack].needsLN2 === true
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
        swapDispatchDewarView: function() {
            this.show_dewars = !this.show_dewars
        }
    },
    mounted: function() {
        setInterval(this.swapDispatchDewarView, 5000)
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