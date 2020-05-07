import Vue from 'vue'
import Router from 'vue-router'

import LoginForm from './components/LoginForm'
import FileArea from './components/FileArea'

Vue.use(Router)

export default new Router({
    mode:'history',
    routes:[
        { path:'/login',component:LoginForm },
        { path:'/filearea',component:FileArea },
    ]
})

