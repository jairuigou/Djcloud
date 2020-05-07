<template>
    <el-container>
        <el-header>
            <el-row class="funcbutton" :gutter="0">
                <el-col :span="1" :offset="19"><el-button class="fbutton" icon="el-icon-search" circle></el-button> </el-col>
                <el-col :span="1"><el-button class="fbutton" type="primary" icon="el-icon-upload" circle @click="dialogUploadVisible = true"></el-button>  </el-col>
                <el-col :span="1"><el-button class="fbutton" type="danger" icon="el-icon-switch-button" circle @click="logout()"></el-button></el-col>
            </el-row>
        </el-header>
        <el-container>
        <el-aside width="50px">
            <el-row>
                <i class="el-icon-folder-opened" @click="viewAreaHook='table'"></i>
            </el-row>
            <el-row>
                <i class="el-icon-picture-outline-round" @click="viewAreaHook='image'"></i>
            </el-row>         
        </el-aside>
        <el-main>
            <el-row v-if="viewAreaHook=='table'">
               <FileTable v-bind:reload="reloadTableFlag"></FileTable>
            </el-row>

            <el-row v-if="viewAreaHook=='image'">
                <ImageView></ImageView>
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
            <el-progress :percentage="uploadProgressval" v-if="uploadProgressVisible==true"></el-progress>
            </el-dialog>
        </el-main>
        </el-container>
        


    </el-container>    

</template>
<script>
import {getcsrftoken,checkstatus} from '../util/core';
import FileTable from "./FileTable";
import ImageView from "./ImageView";
export default {
    components: {
        FileTable,
        ImageView
    },
    data(){
        return{
            dialogUploadVisible:false,
            uploadProgressVisible:false,
            uploadProgressval: 0,
            viewAreaHook:'table',
            reloadTableFlag:false,
        }
    },
    methods:{
        upload(){
            this.$refs.upload.submit();
        },
        uploadfunc(file){
            var token = getcsrftoken('csrftoken');
            var formdata = new FormData();
            formdata.append('csrfmiddlewaretoken',token);
            formdata.append('file',file.file);
            this.uploadProgressVisible = true;
            this.uploadProgressval = 0;
            this.axios({
                url: 'api/uploadsmall',
                method:'post',
                data:formdata,
                headers :{'Content-Type':'application/x-www-form-urlencoded'},
                onUploadProgress: ProgressEvent=>{
                    this.uploadProgressval = Math.round( (ProgressEvent.loaded * 100) / ProgressEvent.total )
                }
            }).then(response =>{
                var status = response.data['status'];
                if(status==='upload_ok'){
                    this.reloadTableFlag = !this.reloadTableFlag;
                    this.dialogUploadVisible = false;
                    this.$refs.upload.clearFiles(); 
                    this.uploadProgressVisible = false;
                }
                else{
                    this.$message.warning(status);
                    this.uploadProgressVisible = false;
                }
            })
            .catch(error =>{
                this.$message.error("upload request error");
                this.uploadProgressVisible = false;
            })
        },
        uploadrequest(file){
            checkstatus().then(status=>{
                if(status === false){
                    this.$message.warning("Login expired");
                    this.$router.push('/login');
                }
                else if (status == 'server error'){
                    this.$message.error(status);
                }
                else{
                    this.uploadfunc(file);
                }
            }) 
        },
        
        logout(){
            var token = getcsrftoken('csrftoken');
            var formdata = new FormData();
            formdata.append('csrfmiddlewaretoken',token);
            formdata.append('status','logout');
            this.axios({
                url: 'api/logout',
                method:'post',
                data:formdata,
                headers :{'Content-Type':'application/x-www-form-urlencoded'}
            }).then(response =>{
                this.$message.success("logout");
                this.$router.push("/login");
            })
            .catch(error =>{
                this.$message.error("logout request error");
            })
        },
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
.el-aside *{
    font-size: 40px;
    color: #909399;
}
.el-aside *:hover{
    color:#409eff;
}


</style>