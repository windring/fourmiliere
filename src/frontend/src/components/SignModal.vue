<template>
  <a-modal type="primary" title="登录/注册" v-model="isShow" centered>
    <a-form>
      <a-form-item>
        <a-input placeholder="昵称" v-model="username">
          <a-icon slot="prefix" type="user"></a-icon>
        </a-input>
      </a-form-item>
      <a-form-item>
        <a-input placeholder="密码" v-model="password">
          <a-icon slot="prefix" type="key"></a-icon>
        </a-input>
      </a-form-item>
      <a-form-item>
        <a-button type="primary" class="sign-button" @click="signIn">登录</a-button>
      </a-form-item>
      <a-form-item>
        <a-button class="sign-button" @click="signUp">注册</a-button>
      </a-form-item>
    </a-form>
    <template slot="footer">
      <span>白云深处有人家</span>
    </template>
  </a-modal>
</template>
<script>
export default {
  name: 'Sign-In-Sign-Up',
  data () {
    return {
      username: '',
      password: '',
    }
  },
  methods: {
    signIn () {
      this.$http.get('user/signin', {
        params: {
          username: this.username,
          password: this.password
        }
      })
      .then((res) => {
        console.log('登录成功')
        console.log(res)
        this.$notification.info({
          message: `欢迎回来 ${res.data.username}`,
          title: 'fourmiliere 留言板'
        })
        this.isShow = false
        this.$store.commit('updateUsername', res.data.username)
      })
      .catch((err) => {
        console.log('登录失败')
        console.log(err.response.data.error)
        this.$notification.error({
          message: 'fourmiliere 留言板',
          description: '登录失败'
        });
      })
    },
    signUp () {
      this.$http.get('user/signup', {
        params: {
          username: this.username,
          password: this.password
        }
      })
      .then((res) => {
        console.log('注册成功')
        console.log(res)
        this.$notification.info({
          message: `注册成功，这是你的用户名 ${res.data.username}`,
          title: 'fourmiliere 留言板'
        })
      })
      .catch((err) => {
        console.log('注册失败')
        console.log(err.response.data.error)
        this.$notification.error({
          message: 'fourmiliere 留言板',
          description: `注册失败，${err.response.data.error}`
        });
      })
    }
  },
  computed: {
    isShow: {
      get () {
        return this.$store.state.showModal
      },
      set (value) {
        this.$store.commit('updateShowModal', value)
      }
    }
  },
}
</script>

<style scoped>
.sign-button {
  width: 100%;
}
.ant-form-item {
  margin-bottom: 10px;
}
</style>
