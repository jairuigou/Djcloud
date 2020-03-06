<template>
    <el-container>
        <el-container>
        <el-aside width="100px"> 
            <el-row class="toptoucharea">
                <el-row type="flex" justify="center" align="middle">
                <i class="el-icon-upload2" @click="toupload()"></i>
                </el-row>
                <el-row type="flex" justify="center">
                <el-button type="text" class="textbutton" @click="toupload()">upload</el-button>
                </el-row>
            </el-row>
            <el-row class="middletoucharea" >
                <el-row type="flex" justify="center" align="middle">
                <i class="el-icon-picture-outline" @click="topicture()"></i>
                </el-row>
                <el-row type="flex" justify="center">
                <el-button type="text" class="textbutton" @click="topicture()">picture</el-button>
                </el-row>
            </el-row>
            <el-row class="middletoucharea" >
                <el-row type="flex" justify="center" align="middle">
                <i class="el-icon-document" ></i>
                </el-row>
                <el-row type="flex" justify="center">
                <el-button type="text" class="textbutton">document</el-button>
                </el-row>
            </el-row>
            <el-row class="middletoucharea" >
                <el-row type="flex" justify="center" align="middle">
                <i class="el-icon-paperclip"></i>
                </el-row>
                <el-row type="flex" justify="center">
                <el-button type="text" class="textbutton">other</el-button>
                </el-row>
            </el-row>
            <el-row class="middletoucharea" >
                <el-row type="flex" justify="center" align="middle">
                <i class="el-icon-refresh " @click="changestatus()"></i>
                </el-row>
                <el-row type="flex" justify="center">
                <el-button type="text" class="textbutton" @click="changestatus()">refresh</el-button>
                </el-row>
            </el-row>
            <el-row class="bottomtoucharea" >
                <el-row type="flex" justify="center" align="middle">
                <i class="el-icon-switch-button" @click="logout()"></i>
                </el-row>
                <el-row type="flex" justify="center">
                <el-button type="text" class="textbutton" @click="logout()">login out</el-button>
                </el-row>
            </el-row>
        </el-aside>
        </el-container>
        <el-container>
        <el-header>
            <el-input v-if="playarea!='upload'" 
                placeholder="search" 
                suffix-icon="el-icon-search" 
                clearable
                class="searchinput"
            ></el-input>
        </el-header>
        <el-main>
            <el-table v-if="playarea=='fileplay'"
            :data="tableData">
            <i class="el-icon-upload"></i>
                <el-table-column label="filename" prop="name">
                </el-table-column>
                <el-table-column label="filetype" prop="type">
                </el-table-column>
                <el-table-column label="filesize" prop="size">
                </el-table-column>
                <el-table-column label="date" prop="date">
                </el-table-column>
            </el-table>

            <div v-if="playarea=='upload'">
            <el-upload
                action=""
                ref="upload"
                :http-request="uploadrequest"
                :auto-upload="false"
                drag
            >
            <i class="el-icon-upload"></i>
            <div class="el-upload__text">Drop file here or<em>click to select</em></div>
            </el-upload>
            <el-button @click="upload()">upload</el-button>
            </div>
        </el-main>
        </el-container>
    </el-container>    
</template>
<script>
export default {
    data(){
        return{
            reloadFlag:false,
            playarea:"fileplay",
            tableData:[]
        }
    },
    mounted:function(){
        this.reloadFlag = !this.reloadFlag;
    },
    watch:{
        reloadFlag:function() {
            this.axios({
                url:'api/infodata',
                method: 'get',
            }).then(response =>{
                var status = response.data['status'];
                if(status == "not_logged"){
                    this.$emit("statuschanged",false);
                }
                else{
                    var data = response.data;
                    var attr = Object.keys(response.data);
                    this.tableData = [];
                    for(var i=0;i<attr.length-1;i++){
                        var tmpOb = {};
                        tmpOb['name'] = data[i]['name'];
                        tmpOb['type'] = data[i]['type'];
                        tmpOb['size'] = data[i]['size'];
                        tmpOb['date'] = data[i]['date'];
                        this.tableData.push(tmpOb);
                    }
                }
            })
            .catch(error=>{
                alert("request error");
            })
        }
    },
    methods:{
        changestatus(){
            this.reloadFlag = !this.reloadFlag;
        },
        toupload(){
            this.playarea = 'upload';
        },
        topicture(){
            this.playarea = 'fileplay';
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
                headers :{'Content-Type':'application/x-www-form-urlencoded'}
            }).then(response =>{
                var status = response.data['status'];
                if(status ==='not_logged')
                    this.$emit("statuschanged",false);
                else if(status==='upload_ok')
                    this.changestatus();
                else
                    console.log(status);
            })
            .catch(error =>{
                console.log("upload request error");
            })
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
                this.$emit("statuschanged",false);
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
.searchinput{
    width: 300px;
}
.toptoucharea{
    margin-top: 10px;
    border-style: solid;
    border-width:1px 1px 1px 1px ; 
    border-color: #ebeef5;
    font-size: 30px;
    color:#606255;
}
.toptoucharea:hover{
    color: #409eff;
}
.toptoucharea:hover .textbutton{
    color:#409eff;
}
.middletoucharea{
    border-style: solid;
    border-width:1px 1px 0px 1px ; 
    border-color: #ebeef5;
    font-size: 30px;
    color:#606255;
}
.middletoucharea:hover{
    color: #409eff;
}
.middletoucharea:hover .textbutton{
    color: #409eff;
}
.bottomtoucharea{
    border-style: solid;
    border-width:1px 1px 1px 1px ; 
    border-color: #ebeef5;
    font-size: 30px;
    color:#606266;
}
.bottomtoucharea:hover{
    color:#409eff;
}
.bottomtoucharea:hover .textbutton{
    color: #409eff;
}
i[class*='el-icon']{
    margin-top: 10px;
}
.textbutton{
    color: #909399;
}
</style>