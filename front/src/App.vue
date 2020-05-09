<template>
  
  <div id="app">
    <router-view/>
  </div>

</template>

<script>
import {checkstatus} from './util/core';
import {mapState} from 'vuex';
export default {
  name: 'App',
  data(){
    return{
    }
  },
  computed:mapState(['loginstatus']),
  watch:{
    loginstatus(newValue,oldValue){
      if(newValue == 'success')
      {
        this.$router.push('filearea');
      }
      else
      {
        this.$router.push('login');
      }
    }
  },
  mounted:function(){
    checkstatus().then(status=>{
      if(status == true){
        this.$store.commit('changeLoginStatus','success');
      }
      else{
        this.$store.commit('changeLoginStatus','error'); 
      }
      if(status == 'server error')
        this.$message.error(status);
    })
  },
  methods:{
  }
}

</script>

<style>

</style>