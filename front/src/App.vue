<template>
  
  <div id="app" >
    <div id="login" v-if="loginstatus==false">
    <h1> DJCLoud</h1>
    <el-row type = "flex" class="loginform" >
        <LoginForm v-on:changestatus="changeloginstatus"></LoginForm>
    </el-row>
    </div>

    <div id="client" v-else>
      <filearea v-on:relogin="relogin"></filearea> 
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
      loginstatus:false,
    }
  },
  beforeCreate:function(){
    this.axios({
      url:'api/checkstatus',
      method:'get',
      headers :{'Content-Type':'application/x-www-form-urlencoded'}
    }).then(response =>{
        var status = response.data['status'];
        if(status === 'not_logged')
          this.loginstatus = false;
        else
          this.loginstatus = true;
    })
  },
  methods:{
    relogin(status){
      this.loginstatus = false;
    },
    changeloginstatus(status){
      this.loginstatus = status;
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