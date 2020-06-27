import Vue from 'vue'
import Admin from './Admin.vue'
import Element from 'element-ui'
import axios from 'axios'
import vueaxios from 'vue-axios'
import 'element-ui/lib/theme-chalk/index.css'

Vue.use(Element)
Vue.use(vueaxios,axios)
Vue.config.productionTip = false

new Vue({
  el: '#admin',
  render: h => h(Admin),
})
