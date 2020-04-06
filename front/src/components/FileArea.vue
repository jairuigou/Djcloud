<template>
    <el-container>
        <el-main>
            <el-row class="funcbutton" :gutter="0">
                <el-col :span="1" :offset="19"><el-button class="fbutton" icon="el-icon-search" circle></el-button> </el-col>
                <el-col :span="1"><el-button class="fbutton" type="primary" icon="el-icon-upload" circle @click="dialogUploadVisible = true"></el-button>  </el-col>
                <el-col :span="1"><el-button class="fbutton" type="danger" icon="el-icon-switch-button" circle @click="logout()"></el-button></el-col>
            </el-row>

            <el-row>
               <FileTable v-on:relogin="relogin" v-bind:reload="reloadTableFlag"></FileTable>
            </el-row>

            <el-dialog title="Upload File" :visible.sync="dialogUploadVisible">
            <el-upload action=""
                ref="upload" 
                :http-request="uploadrequest"
                :auto-upload="false"
                drag
            >
            <i class="el-icon-upload"></i>
            <div class="el-upload__text">Drop file here or<em>click to select</em></div>
            </el-upload>
            <el-button @click="upload()">upload</el-button>
            </el-dialog>
        </el-main>


    </el-container>    

</template>
<script>
import FileTable from "./FileTable"
export default {
    components: {
        FileTable
    },
    data(){
        return{
            dialogUploadVisible:false,
            reloadTableFlag:false,
        }
    },
    methods:{
        relogin(status){
            this.$emit("relogin",true);
        },
        upload(){
            this.$refs.upload.submit();
        },
        uploadrequest(file){
            var token = this.getcsrftoken('csrftoken');
            var formdata = new FormData();
            formdata.append('csrfmiddlewaretoken',token);
            formdata.append('file',file.file);
            this.axios({
                url: 'api/uploadsmall',
                method:'post',
                data:formdata,
                headers :{'Content-Type':'application/x-www-form-urlencoded'},
                onUploadProgress: ProgressEvent=>{
                    console.log(Math.round( (ProgressEvent.loaded * 100) / ProgressEvent.total ));
                }
            }).then(response =>{
                var status = response.data['status'];
                if(status ==='not_logged')
                    this.$emit("relogin",true);
                else if(status==='upload_ok')
                    this.reloadTableFlag = !this.reloadTableFlag;
                else
                    this.$message.error(status);   
            })
            .catch(error =>{
                this.$message.error("upload request error");
            })
            this.dialogUploadVisible = false;
        },
        logout(){
            var token = this.getcsrftoken('csrftoken');
            var formdata = new FormData();
            formdata.append('csrfmiddlewaretoken',token);
            formdata.append('status','logout');
            this.axios({
                url: 'api/logout',
                method:'post',
                data:formdata,
                headers :{'Content-Type':'application/x-www-form-urlencoded'}
            }).then(response =>{
                this.$emit("relogin",true);
            })
            .catch(error =>{
                console.log("logout request error");
            })
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
        }
    }
}
</script>
<style scoped>
.funcbutton{
    margin-top: 20px;
    margin-bottom: 5px;
}
.fbutton{
    font-size: 15px;
}


</style>