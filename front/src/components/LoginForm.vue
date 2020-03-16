<template>
    <el-card class="login-card">
        <div slot="header" class="head">
            <span>Login</span>
        </div>
        <div>
            <el-form :model="form" status-icon :rules="rules" ref="form">
            <el-form-item label="Username" prop="username">
            <el-input
                placeholder="Enter Username"
                v-model="form.username"
                clearable
            >
            </el-input>
            </el-form-item>
            <el-form-item label="Password" prop="password">
            <el-input
                placeholder="Enter Password" 
                v-model="form.password" 
                show-password
                clearable
            >
            </el-input> 
            </el-form-item>
            <el-form-item>
                <el-button type="primary" :loading=bloading @click="onSubmit('form')">Sign in</el-button>
            </el-form-item>
            </el-form>
        </div>
    </el-card>    
</template>
<script>
export default {
    data(){
        var validateUser = (rule,value,callback)=>{
            if(value===''){
                callback(new Error('Username can not be empty'));
            }
            else{
                callback();
            }
        };
        var validatePass = (rule,value,callback)=>{
            if(value===''){
                callback(new Error('Password can not be empty'));
            }
            else{
                callback();
            }
        };
        return{
            bloading :false,
            form:{
                username:'',
                password:'',
            },
            rules:{
                username:[
                    { validator: validateUser, trigger: 'blur' }
                ],
                password:[
                    { validator: validatePass, trigger: 'blur' }
                ]
            }
        };
    },
    
    methods:{
        onSubmit(formName){
            this.$refs[formName].validate((valid)=>{
                if(valid){
                    this.bloading = true;
                    var token = this.getcsrftoken('csrftoken');
                    var formdata = new FormData();
			        formdata.append('username',this.form.username);
			        formdata.append('password',this.form.password);
			        formdata.append('csrfmiddlewaretoken',token);
			        this.axios({
				        url: 'api/verify',
				        method: 'post',
				        data: formdata,
				        headers :{'Content-Type':'application/x-www-form-urlencoded'}
			        }).then(response => {
                        var status = response.data['status'];
                        if(status == "login_ok" || status == "logged"){
                            this.$message.success("Success");
                            this.$emit('statuschanged',true);
                        }
                        else{
                            this.bloading=false;
                            this.$message.error("Incorrect username or password");
                        }
                    })
                    .catch(error=>{
                        this.$message.error("request error");
                    }) 
                }
                else{
                    return;
                }
            });
        },
        getcsrftoken: function(name){
            if(document.cookie && document.cookie!=''){
                var cookies = document.cookie.split(';');
                for( var i=0;i<cookies.length;i++){
                    var cookie = cookies[i];
                    var kk = cookie.split('=');
                    if( kk[0] == name){
                        return kk[1];
                    }
                } 
            }
            return "";
        },
        
    }

}
</script>
<style scoped>
.login-card{
    width:330px;
    height:350px
}
</style>