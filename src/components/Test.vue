<template>
<!-- 模板  html -->
    <div>
        <p :style="{ fontSize: '60px', fontFamily: 'Arial', color: 'black' }">欢迎来到PM界面</p>
       
    </div>
</template>

<script>
// js  逻辑
export default{
    name:"Test",  //组件名
    data(){   // 数据
        return{
            str1:"欢迎来到PM界面",
            str2:""
        }
    }
}



</script>

<style scoped>
    div{
        text-align:center
    }
    .str1{
        font-size:200px;
    }
</style>