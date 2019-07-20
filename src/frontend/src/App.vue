<template>
  <a-layout id="app">
    <a-layout-header>
      <a-menu theme="dark" mode="horizontal" class="header-menu">
        <a-menu-item key="1">首页</a-menu-item>
        <a-menu-item key="2" @click="showModal">登录 / 注册</a-menu-item>
      </a-menu>
    </a-layout-header>
    <a-layout-content class="content-box">
      <hello-world class="content"></hello-world>
    </a-layout-content>
    <a-layout-footer class="text-center">
      fourmilière frontend @2019 windring
    </a-layout-footer>
    <sign-modal></sign-modal>
    <check-sign></check-sign>
  </a-layout>
</template>

<script>
import HelloWorld from './components/HelloWorld.vue'
import SignModal from './components/SignModal.vue'
import CheckSign from './components/CheckSign.vue'

export default {
  name: 'app',
  data () {
    return {
    }
  },
  components: {
    HelloWorld,
    SignModal,
    CheckSign,
  },
  methods: {
    showModal () {
      this.$store.commit('updateShowModal', true)
    }
  },
}
</script>

<style scoped>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  min-height: 100vh;
}
.text-center {
  text-align: center;
  color: #2c3e50;
}
.content-box {
  padding: 64px 50px;
  min-height: calc(100vh - 134px);
  display: flex;
  flex-direction: column;
}
.content {
  padding: 24px;
  background: #fff;
  flex-grow: 1;
}
.header-menu {
  line-height: 64px !important;
}
</style>
