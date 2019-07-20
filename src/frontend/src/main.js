import Vue from 'vue'
import App from './App.vue'
import Antd from 'ant-design-vue'
import axios from 'axios'
import VueAxios from 'vue-axios'
import 'ant-design-vue/dist/antd.css'
import store from './store'

Vue.config.productionTip = false

Vue.use(Antd)
Vue.use(VueAxios, axios)

new Vue({
  store,
  render: h => h(App)
}).$mount('#app')
