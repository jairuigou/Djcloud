// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import Element from 'element-ui'
import axios from 'axios'
import vueaxios from 'vue-axios'
import 'element-ui/lib/theme-chalk/index.css'
Vue.use(Element)
Vue.use(vueaxios,axios)
Vue.config.productionTip = false
/* eslint-disable no-new */
new Vue({
  el: '#app',
  components: { App },
  template: '<App/>'
})
