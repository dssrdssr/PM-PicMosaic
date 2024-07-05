<template>
  <div>
      <el-container>
      <el-header>上传图片</el-header>
      <el-container>
      <el-aside width="200px">
          <button @click="upload">
          点击上传
          </button>
      </el-aside>
      <el-main>
          <el-upload class="upload-demo" drag action="https://jsonplaceholder.typicode.com/posts/" multiple>
          <i class="el-icon-upload"></i>
          <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
          <div class="el-upload__tip" slot="tip">只能上传jpg/png文件，且不超过500kb</div>
      </el-upload>
      </el-main>
      </el-container>
      </el-container>
  </div>
</template>

<script>

  export default {
      name:"Element",  // 组件名
      data(){   // 数据
          return{
             
          }
      },
      components:{

      },   //注册子组件
      methods:{   //声明普通函数
          async upload(){
          
          }
      },
      mounted(){
          console.log(this.$router.options.routes);
      }

  }
</script>

<style scoped>
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
.el-upload{
  text-align: center;
  position: absolute;
}
</style>