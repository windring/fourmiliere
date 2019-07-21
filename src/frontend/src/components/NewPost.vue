<template>
  <a-form>
    <a-form-item>
      <a-textarea placeholder="输入留言内容" :rows="4" v-model="post"/>
    </a-form-item>
    <a-form-item>
      <a-button type="primary" @click="newpost">留言</a-button>
    </a-form-item>
  </a-form>
</template>
<script>
export default {
  name: 'NewPost',
  data () {
    return {
      post: ''
    }
  },
  methods: {
    newpost () {
      if (!this.$store.state.loginState) {
        this.$notification.info({
          message: '请先登录',
          title: 'fourmiliere 留言板'
        })
        return
      }
      this.$http.get('post/new/', {
        params: {
          create_time: new Date().getTime(),
          content: this.post
        }
      }).then((res) => {
        this.$notification.info({
          message: '发布成功',
          title: 'fourmiliere 留言板'
        })
        // console.log(res)
      }).catch((err) => {
        this.$notification.error({
          message: '留言失败',
          title: 'fourmiliere 留言板'
        })
        // console.log(err)
      })
    }
  }
}
</script>
