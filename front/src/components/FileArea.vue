<template>
    <el-container>
        <el-main>
            <el-row class="funcbutton">
                <el-button class="fbutton" icon="el-icon-search" circle></el-button> 
                <el-button class="fbutton" type="primary" icon="el-icon-upload" circle @click="toupload()"></el-button>  
                <el-button class="fbutton" type="danger" icon="el-icon-switch-button" circle @click="logout()"></el-button>
            </el-row>
            <el-row v-if="playarea=='fileplay'">
                <el-table 
                :data="tableData">
                    <el-table-column label="Filename" prop="name">
                    </el-table-column>
                    <el-table-column label="Filetype" prop="type"
                        :filters="typefilt"
                        :filter-method="typefiltmethod">
                    </el-table-column>
                    <el-table-column label="Filesize" prop="size"
                        sortable>
                    </el-table-column>
                    <el-table-column label="Date" prop="date">
                    </el-table-column>
                    <el-table-column label="Operations">
                        <template slot-scope="scope">
                            <el-button size='mini' type="primary" icon="el-icon-download" circle
                            @click="handleDownload(scope.row)"></el-button>
                            <el-button size='mini' type="danger" icon="el-icon-delete" circle
                            @click="handleDelete(scope.row)"></el-button>
                        </template>
                    </el-table-column>
                </el-table>
            </el-row>

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
</template>
<script>
export default {
    data(){
        return{
            reloadFlag:false,
            playarea:"fileplay",
            tableData:[],
            typefilt:[{ text: 'PNG', value: 'PNG' }, { text: 'jpg', value: 'jpg' }]
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
                    this.typefilt = [];
                    this.typefilt.pushone = function(tmp){
                        for(var i=0;i<this.length;i++)
                        {
                            if(tmp['text'] == this[i]['text'])
                                break;
                        }
                        if(i==this.length)
                            this.push(tmp);
                    };
                    for(var i=0;i<attr.length-1;i++){
                        var tmpOb = {},tmpOb1={};
                        tmpOb['name'] = data[i]['name'];
                        tmpOb['type'] = data[i]['type'];
                        tmpOb['size'] = data[i]['size'];
                        tmpOb['date'] = data[i]['date'];
                        this.tableData.push(tmpOb);
                        tmpOb1['text'] = data[i]['type'];
                        tmpOb1['value'] = data[i]['type'];
                        this.typefilt.pushone(tmpOb1);
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
        typefiltmethod(value,row){
            return row.type === value;
        },
        handleDownload(row){
            console.log(row); 
        },
        handleDelete(row){
            var token = this.getcsrftoken('csrftoken');
            var formdata = new FormData();
            formdata.append('csrfmiddlewaretoken',token);
            formdata.append('file',row['name']);
            this.axios({
                url: 'api/remove',
                method:'post',
                data:formdata,
                headers :{'Content-Type':'application/x-www-form-urlencoded'}
            }).then(response =>{
                var status = response.data['status'];
                if(status ==='not_logged')
                    this.$emit("statuschanged",false);
                else if(status==='delete_ok')
                    this.changestatus();
                else
                    console.log(status);
            })
            .catch(error =>{
                console.log("delete request error");
            })
        },
        toupload(){
            this.playarea = 'upload';
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
.funcbutton{
    margin-top: 10px;
    margin-bottom: 10px;
}
.fbutton{
    font-size: 20px;
}
</style>