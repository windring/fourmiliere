import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    username: '',
    loginState: false,
    showModal: false
  },
  mutations: {
    updateShowModal (state, showModal) {
      state.showModal = showModal
    },
    updateUsername (state, username) {
      state.username = username
      state.loginState = !state.loginState
    }
  },
  actions: {

  }
})
