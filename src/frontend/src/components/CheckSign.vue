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
            console.log(res)
          })
          .catch((err) => {
            console.log(err)
            this.openNotification()
          })
      })
    },
  }
</script>
