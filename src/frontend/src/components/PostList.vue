<template>
  <a-list itemLayout="vertical" size="large" :pagination="pagination" :dataSource="listData" :loading="isLoading">
    <a-list-item slot="renderItem" slot-scope="item, index" :key="index">
      <template slot="actions">
        <span @click="like(item.id, item)">
          <a-icon type="like" style="margin-right: 8px" />
          {{ item.like }}
        </span>
        <span @click="hate(item.id, item)">
          <a-icon type="dislike" style="margin-right: 8px" />
          {{ item.hate }}
        </span>
      </template>
      <a-list-item-meta :description="new Date(item['create_time']).toLocaleString()">
        <a slot="title" :href="item.href">{{item.username}}</a>
        <a-avatar slot="avatar"/>
      </a-list-item-meta>
      {{item.content}}
    </a-list-item>
  </a-list>
</template>
<script>

export default {
  data () {
    return {
      isLoading: true,
      listData: [],
      pagination: {
        onChange: () => {
          // console.log(page);
        },
        pageSize: 10,
      },
    }
  },
  methods: {
    like (id, item) {
      this.$http.get('post/like/', {
        params: {
          pid: id
        }
      }).then((res) => {
        // console.log(res)
        item.like = res.data.like
        item.hate = res.data.hate
      }).catch((err) => {
        this.$notification.error({
          message: `点赞失败, ${err}`,
          title: 'fourmiliere 留言板'
        })
      })
    },
    hate (id, item) {
      this.$http.get('post/hate/', {
        params: {
          pid: id
        }
      }).then((res) => {
        // console.log(res)
        item.hate = res.data.hate
        item.like = res.data.like
      }).catch(() => {
        this.$notification.error({
          message: '踩留言失败',
          title: 'fourmiliere 留言板'
        })
      })
    },
    loadData () {
      this.$http.get('post/all/', {
        params: {
        }
      }).then((res) => {
        const listData = JSON.parse(res.data).map(i => {
          i.fields.id = i.pk
          return i.fields
        })
        this.listData = listData.sort((a, b) => b['create_time'] - a['create_time'])
        this.isLoading = false
        // console.log(this.listData)
      })
    },
  },
  mounted () {
    const vm = this
    this.$nextTick(() => {
      vm.loadData()
    })
  }
}
</script>
<style>

</style>