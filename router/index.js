import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '@/pages/Home.vue'
import Heros from '@/pages/Login.vue'
import Function from '@/pages/Function.vue'

Vue.use(VueRouter)

// 创建路由实例对象 
export default new VueRouter({
    // 路由  key（url地址）  ----> value（组件）
    routes:[   // 路由 配置
        {
            path:"/",  //路由地址
            component:Home,  //路由对应的组件
            meta:{  //路由元信息
                name:"首页",   // 路由导航名称
                isShow:true
            }
        },
        {
            path:"/login",
            component:Heros,
            meta:{
                name:"登录",
                isShow:true
            }
        },
        {
            path:"/function",
            component:Function,
            meta:{
                name:"使用",
                isShow:true
            }
        }
    ]
})