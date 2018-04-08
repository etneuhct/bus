import Vue from 'vue'
import App from './App.vue'
import AnimatedVue from 'animated-vue'
import VueSocketio from 'vue-socket.io'
import './assets/bubble.css'
import 'animate.css/animate.css'

Vue.use(AnimatedVue);
Vue.use(VueSocketio, 'http://localhost:3001');

new Vue({
  el: '#app',
  render: h => h(App)
})
