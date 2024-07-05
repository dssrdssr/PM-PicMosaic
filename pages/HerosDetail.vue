<template>
    <div class="heros-con">
       <div class="heros-left">
           <img :src="`http://cdn.xiaohigh.com/${hero.image}`" alt="" />
           <h2>{{hero.name}}</h2>
           <h3>{{hero.type}}</h3>
           <div class="img-min">
               <ul>
                   <li v-for="(item,index) in hero.skills" :key="index">
                       <img :src="`http://cdn.xiaohigh.com/${item.img}`" alt="" />
                       <h4>{{item.name}}</h4>
                   </li>
                   
               </ul>
           </div>
       </div>
       <div class="heros-right">
           <img :src="`http://cdn.xiaohigh.com/${hero.big_image}`" alt="" />
           <hr />
           <p v-html="hero.intro"></p>
       </div>
   </div>
</template>

<script>
   export default {
       name:"HerosDetail",
       data(){
           return{
               hero:{}
           }
       },
       async mounted(){
           // console.log(this.$route.query.id);

           let {data} = await this.$axios.get(`http://api.xiaohigh.com/heros/${this.$route.query.id}`);
           // console.log(data);
           this.hero = data;
       }
   }
</script>

<style>
  .el-header, .el-footer {
    background-color: #B3C0D1;
    color: #333;
    text-align: center;
    line-height: 60px;
  }
  
  .el-aside {
    background-color: #D3DCE6;
    color: #333;
    text-align: center;
    line-height: 200px;
  }
  
  .el-main {
    background-color: #E9EEF3;
    color: #333;
    text-align: center;
    line-height: 160px;
  }
  
  body > .el-container {
    margin-bottom: 40px;
  }
  
  .el-container:nth-child(5) .el-aside,
  .el-container:nth-child(6) .el-aside {
    line-height: 260px;
  }
  
  .el-container:nth-child(7) .el-aside {
    line-height: 320px;
  }
</style>