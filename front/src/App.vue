<template>
  
  <div id="app" >
    <div id="login" v-if="logstatus===false">
    <h1> DJCLoud</h1>
    <el-row type = "flex" class="loginform" >
        <LoginForm v-on:statuschanged="changestatus"></LoginForm>
    </el-row>
    </div>

    <div id="client" v-else>
      <filearea ></filearea> 
    </div>
  </div>

</template>

<script>
import LoginForm from './components/LoginForm'
import filearea from './components/FileArea'
export default {
  name: 'App',
  components: {
    LoginForm,
    filearea
  },
  data(){
    return{
      logstatus:false,
    }
  },
  methods:{
    changestatus:function(status){
      this.logstatus = status;
    }
  }
}

</script>

<style>
h1{
  color :rgb(0, 174, 255);
  font-size: 100px;
  font-weight: 900;
  text-align: center;
  letter-spacing: 20px;
}
.loginform{
    justify-content: center; /* 水平居中 */

}
</style>