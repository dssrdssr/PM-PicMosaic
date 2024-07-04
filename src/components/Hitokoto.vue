<template>
    <div>
        <button  style="display:block;margin:0 auto" @click="getValue">
            <p v-if="!flag">点击显示介绍</p>
            <p v-if="flag">点击关闭介绍</p>
        </button>

        <p style="text-indent:2em;">{{ str }}</p>
    </div>
    
</template>

<script>
    export default {
        name:"Hitokoto",
        data(){
            return{
                str:"",
                flag:0
            }
        },
        methods:{
            // 后台返回 数据   一定是 json 对象

            //  浏览器 同源策略
            //  https://  url +  端口号

            //  https:// localhost:8080
            //  https:// 127.0.0.1:8080

           /*  {
                data:{},
                code:
                message:""
            } */
            //请求api 获取数据
            //  https://v1.hitokoto.cn/
            async getValue(){
                //  this  指向当前组件
                // get  post  put  delete  
                // console.log(this);
                // let  声明变量
                //  const  常量
                //  var  声明变量  慢慢弃用
                if (this.flag==0)
                {
                    this.str = "为了应对许多图片、视频处理工作者批量打码的需求，此网站可以上传视频或批量上传图片，并由用户框选区域。最后通过检测区域内是否有敏感或隐私信息，来对图片或视频进行打码并提供下载。";
                    this.flag=1;
                }
                else if (this.flag==1)
                {
                    this.str = "";
                    this.flag=0;
                }
               
            }
        }
    }
</script>

<style scoped>
button{
    width: 300px;
    height: 60px;
    background: beige;
    text-align:center
}
</style>