<template>
  
  <div id="app">
    <router-view/>
  </div>

</template>

<script>
import {checkstatus} from './util/core'
export default {
  name: 'App',
  data(){
    return{
    }
  },
  mounted:function(){
    checkstatus().then(status=>{
      if(status == true)
        this.$router.push('./filearea');
      else
        this.$router.push('/login')
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