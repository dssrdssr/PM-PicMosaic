import Vue from 'vue'
import App from './App.vue'
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';

Vue.use(ElementUI);
Vue.config.productionTip = false


//导入 axios
import axios from "axios";

// 将 axios 注册全局    原型  --->  原型链    【继承】 
Vue.prototype.$axios = axios;

//导入路由
import router from "@/router"

new Vue({
  render: h => h(App),
  router
}).$mount('#app')


// index.html  --->  main.js   --->  app.vue
