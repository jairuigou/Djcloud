<template>
    <div id="app">
        <LoginForm v-if="change == true"></LoginForm>
        <AdminView></AdminView>
    </div>
</template>

<script>
import {mapState} from 'vuex';
import LoginForm from '../../components/LoginForm';
import AdminView from './components/AdminView';
export default {
    name: 'App',
    components:{
        LoginForm,
        AdminView
    },
    data(){
        return {
            change: false
        }
    }
}
</script>
<style>

</style>