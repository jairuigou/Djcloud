import Vue from 'vue'
import App from './App.vue'
import Element from 'element-ui'
import axios from 'axios'
import vueaxios from 'vue-axios'
import 'element-ui/lib/theme-chalk/index.css'
import router from './router'
import store from './store'

Vue.use(Element)
Vue.use(vueaxios,axios)
Vue.config.productionTip = false



new Vue({
  render: h => h(App),
  router,
  store,
}).$mount('#app')
