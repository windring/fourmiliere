<template>
  <a-layout id="app">
    <a-layout-header>
      <a-menu theme="dark" mode="horizontal" class="header-menu">
        <a-menu-item key="1">首页</a-menu-item>
        <a-menu-item key="2" @click="showModal" v-if="!this.$store.state.loginState">登录 / 注册</a-menu-item>
        <a-menu-item key="3" @click="signout" v-if="this.$store.state.loginState">登出</a-menu-item>
      </a-menu>
    </a-layout-header>
    <a-layout-content class="content-box">
      <new-post></new-post>
      <a-divider>fourmiliere 留言板</a-divider>
      <post-list></post-list>
    </a-layout-content>
    <a-layout-footer class="text-center">
      fourmilière frontend @2019 windring
    </a-layout-footer>
    <sign-modal></sign-modal>
    <check-sign></check-sign>
  </a-layout>
</template>

<script>
import SignModal from './components/SignModal.vue'
import CheckSign from './components/CheckSign.vue'
import PostList from './components/PostList.vue'
import NewPost from './components/NewPost.vue'

export default {
  name: 'app',
  data () {
    return {
    }
  },
  components: {
    SignModal,
    CheckSign,
    PostList,
    NewPost
  },
  methods: {
    showModal () {
      this.$store.commit('updateShowModal', true)
    },
    signout () {
      this.$http.get('user/signout/')
        .then(() => {
          window.reload()
        })
        .catch(() => {
          this.$notification.error({
            message: '登出失败',
            title: 'fourmiliere 留言板'
          })
        })
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
  padding: 64px 10vw;
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
