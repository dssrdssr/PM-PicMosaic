<template>
  <!-- 模板   html   -->
  <div id="app">

    <!-- <router-link to="/">首页</router-link>
    <router-link to="/heros">英雄</router-link> -->
    <ul>
    
    <template v-for="(item,index) in $router.options.routes">
    <router-link :key="index" :to="item.path"  v-if="item.meta.isShow"   ><li>{{ item.meta.name }}</li></router-link>
    </template>
    
    </ul>
    <!-- 路由组件占位 -->
    <router-view />
    
  </div>
</template>

<script>
// 逻辑   js   javascript 
export default {
  name: 'App',   // 组件名
  mounted(){
    console.log(this.$router.options.routes);
  }
  
}
</script>

<style scoped>
   *{
    margin: 0;
    padding: 0;
   }

   ul{
    list-style: none;
    background: black;
    color: white;
    font-size: 30px;
    display: flex;
    flex-wrap: wrap;
    justify-content: space-around;
    height: 80px;
    line-height: 80px;
   }

   ul>li{
    display: inline-block;
    width: 20%;
    text-align: center;
   }

   ul>li:hover{
    cursor: pointer;
    background: gainsboro;
   }

   /* class  选择器 */
   .active{
    background: goldenrod;
   }

    
</style>
