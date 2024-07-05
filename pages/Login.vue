<template>
    <div class="login_container">
        <div class="login_box">
            <br/><br/>
            <input v-model="keyword" type="text" placeholder="Id" />
            <br/><br/><br/>
            <input v-model="keyword" type="text" placeholder="Password" />
            <br/><br/><br/>
            <ul>
            <li>
            <button @click="login">登录</button>
            </li>
            <li>
            <button @click="register">注册</button>
            </li>
        
            </ul>
        </div>
    </div>
</template>

<script>
export default {
    name:"Heros",   //组件名
    data() {
        return {
            // 表单数据对象
            loginForm: {
            username: "admin",
            password: "123456",
            }
        }
    },
    methods:{   // 普通函数 方法
        async login(){
            console.log(this);
        },
        async register(){
            console.log(this);
        }
    }
}
</script>

<style scoped>
 .login_container{
        text-align:center;
        background-color: lightcoral;
        height: 100%;
    }
.login_box {
    width: 450px;
    height: 250px;
    background: #e4f12b;
    border-radius: 3px;
    box-shadow: 0 0 10px #ddd;
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
}
ul{
    list-style: none;
    background: rgb(42, 153, 180);
    color: white;
    font-size: 30px;
    display: flex;
    flex-wrap: wrap;
    justify-content: space-around;
    height: 60px;
    line-height: 40px;
   }

   ul>li{
    display: inline-block;
    width: 20%;
    text-align: center;
   }
</style>