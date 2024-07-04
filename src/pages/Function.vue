<template>
    <div class="login_container">
    <div class="login_box">
    <!-- 头像区域 -->
    <div class="avatar_box">
      <img src="../assets/logo.png" alt="" />
    </div>
    <!-- 登录表单 -->
    <el-form
      :model="loginForm"
      :rules="rules"
      label-width="0px"
      class="login_form"
      ref="LoginFormRef"
    >
      <el-form-item prop="username">
        <el-input
          v-model="loginForm.username"
          prefix-icon="iconfont icon-user"
        ></el-input>
      </el-form-item>
      <el-form-item prop="password">
        <el-input
          v-model="loginForm.password"
          prefix-icon="iconfont icon-3702mima"
        ></el-input>
      </el-form-item>
      <el-form-item class="btns">
        <el-button
          type="primary"
          round
          style="background-color: lightcoral; border: 1px solid #eee"
          @click="login"
          >登录</el-button
        >
        <el-button
          type="info"
          round
          style="background-color: #ddd; border: 1px solid #eee"
          @click="resetForm"
          >重置</el-button
        >
        </el-form-item>
        </el-form>
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
        async resetForm(){
            console.log(this);
        }
    }
}
</script>

<style lang="less" scoped>
.login_container {
background-color: lightcoral;
height: 100%;
}
.login_box {
width: 450px;
height: 300px;
background: #fff;
border-radius: 3px;
box-shadow: 0 0 10px #ddd; //阴影
position: absolute;
left: 50%;
top: 50%;
transform: translate(-50%, -50%);
 .avatar_box {
height: 130px;
width: 130px;
border: 1px solid #eee;
border-radius: 50%;
padding: 10px; //头像图片和头像盒子的距离
box-shadow: 0 0 10px #ddd;
position: absolute;
left: 50%;
transform: translate(-50%, -50%);
background-color: #fff;
}
.avatar_box img {
width: 100%;
height: 100%;
border-radius: 50%;
background-color: #eee;
}

}
.login_form {
position: absolute;
bottom: 0;
width: 100%;
padding: 0 20px;
box-sizing: border-box;
}
.btns {
display: flex;
justify-content: flex-end;
background-color: #eee;
}
</style>