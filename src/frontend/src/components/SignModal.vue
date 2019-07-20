<template>
  <a-modal type="primary" title="登录/注册" v-model="isShow" centered>
    <a-form>
      <a-form-item>
        <a-input placeholder="昵称" v-model="nickname">
          <a-icon slot="prefix" type="user"></a-icon>
        </a-input>
      </a-form-item>
      <a-form-item>
        <a-input placeholder="密码" v-model="password">
          <a-icon slot="prefix" type="key"></a-icon>
        </a-input>
      </a-form-item>
      <a-form-item>
        <a-button type="primary" class="sign-button">登录</a-button>
      </a-form-item>
      <a-form-item>
        <a-button class="sign-button">注册</a-button>
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
      nickname: '',
      password: '',
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
