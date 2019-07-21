<template>
  <div></div>
</template>

<script>
  export default {
    methods: {
      openNotification () {
        this.$notification.open({
          message: 'fourmiliere 留言板',
          description: '您好，欢迎来访，请先注册 / 登录。',
          icon: <a-icon type="smile" style="color: #108ee9" />,
        })
      },
    },
    mounted () {
      this.$nextTick(() => {
        this.$http.get('user/auth/')
          .then((res) => {
            // console.log(res)
            this.$store.commit('updateUsername', res.data.username)
            this.$notification.info({
              message: `${res.data.username} 你好，你已经登录。`,
              title: 'fourmiliere 留言板'
            })
          })
          .catch(() => {
            // console.log(err)
            this.openNotification()
          })
      })
    },
  }
</script>
