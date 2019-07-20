import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    nickname: '',
    loginState: '',
    showModal: false,
  },
  mutations: {
    updateShowModal (state, showModal) {
      state.showModal = showModal
    }
  },
  actions: {

  }
})
