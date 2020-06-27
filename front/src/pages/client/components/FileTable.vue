<template>

<el-table 
:data="tableData"
stripe
>
    <el-table-column label="Filename" prop="name">
    </el-table-column>
    <el-table-column label="Filetype" prop="type"
        :filters="typefilt"
        :filter-method="typefiltmethod">
    </el-table-column>
    <el-table-column label="Filesize" prop="size"
        sortable>
    </el-table-column>
    <el-table-column label="Date" prop="date" >
    </el-table-column>
    <el-table-column label="Operations">
        <template slot-scope="scope">
            <el-button size='mini' icon="el-icon-view" circle
            @click="handleView(scope.row)"></el-button>

            <el-progress type="circle" 
                width=30
                stroke-width=2
                style="margin-left:10px;margin-top:0px;margin-bottom:0px"
                :percentage="scope.row.downloadprecentage" v-if="scope.row.progressvisible">
            </el-progress>
            <el-button size='mini' type="primary" icon="el-icon-download" circle v-else
            @click="handleDownload(scope.row)"></el-button>

            <el-popover
            placement="bottom"
            width="200"
            trigger="click"
            v-model="scope.row.tipvisible"
            style="margin-left:10px"
            >
            <p> <i class="el-icon-info" style="color:red"></i> Sure to delete this?</p>
                <div style="text-align:right;margin:0">
                    <el-button size="mini" type="text" @click="scope.row.tipvisible=false;">cancel</el-button>
                    <el-button type="primary" size="mini" @click="handleDelete(scope.row)">confirm</el-button>
                </div>
            <el-button slot="reference"
                size='mini'
                type='danger'
                icon="el-icon-delete"
                circle
            ></el-button>
            </el-popover>
        </template>
    </el-table-column>
</el-table>

</template>
<script>
import {getcsrftoken,checkstatus} from "../../../util/core";
export default {
    data(){
        return{
            reloadFlag:false,
            tableData:[],
            typefilt:[]
        }
    },
    props:{
        reload : Boolean,
    },
    mounted:function(){
        this.reloadFlag = !this.reloadFlag;
    },
    watch:{
        reload:function(){
            this.reloadFlag = !this.reloadFlag;
        },
        reloadFlag:function() {
            this.axios({
                url:'api/infodata',
                method: 'get',
            }).then(response =>{
                var status = response.data['status'];
                if(status == "not_logged"){
                    this.$store.commit('changeLoginStatus','error');
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
                        tmpOb['filename'] = data[i]['filename'];
                        tmpOb['name'] = data[i]['name'];
                        tmpOb['type'] = data[i]['type'];
                        tmpOb['size'] = data[i]['size'];
                        tmpOb['date'] = data[i]['date'];
                        tmpOb['tipvisible'] = false;
                        tmpOb['progressvisible'] = false;
                        tmpOb['downloadprecentage'] = 0;
                        this.tableData.push(tmpOb);
                        tmpOb1['text'] = data[i]['type'];
                        tmpOb1['value'] = data[i]['type'];
                        this.typefilt.pushone(tmpOb1);
                    }
                }
            })
            .catch(error=>{
                this.$$message.error("load data request error");
            })
        }
    },
    methods:{
        typefiltmethod(value,row){
            return row.type === value;
        },
        handleView(row){
            checkstatus().then(status=>{
                if(status === false){
                    this.$message.warning("Login expired");
                    this.$store.commit('changeLoginStatus','error');
                }
                else if (status == 'server error'){
                    this.$message.error(status);
                }
                else{
                    if(row['type'] == 'jpg'){
                        this.download(row['filename'],1,row);
                    }
                    else{
                    this.download(row['filename'],2,row);
                    }
                }
            }) 
        },
        handleDownload(row){
            checkstatus().then(status=>{
                if(status === false){
                    this.$message.warning("Login expired");
                    this.$store.commit('changeLoginStatus','error');
                }
                else if (status == 'server error'){
                    this.$message.error(status);
                }
                else{
                    this.download(row['filename'],0,row);
                }
            }) 
        },
        download(filename,method,row){
            row.downloadprecentage = 0;
            var token = getcsrftoken('csrftoken');
            var formdata = new FormData();
            formdata.append('csrfmiddlewaretoken',token);
            formdata.append('file',filename);
            this.axios({
                url: 'api/download',
                method:'post',
                data:formdata,
                headers :{'Content-Type':'application/x-www-form-urlencoded'},
                responseType:'blob',
                onDownloadProgress: ProgressEvent=>{
                    row.downloadprecentage =  Math.round( (ProgressEvent.loaded * 100) / ProgressEvent.total );
                }
            }).then(response =>{
                var elink = document.createElement('a');
                var blob;
                if(method === 0){
                    elink.download = filename;
                    blob = new Blob([response.data]);
                }
                else if(method===1){
                    blob = new Blob([response.data],{type:"image/jpeg"});
                }
                else{
                    blob = new Blob([response.data]);
                }
                var url = URL.createObjectURL(blob);
                elink.style.display = 'none';
                elink.href = url;
                document.body.appendChild(elink);
                elink.click();
                URL.revokeObjectURL(elink.href);
                document.body.removeChild(elink);
            })
            .catch(error =>{
                this.$message.error("download error");
            })
        },
        handleDelete(row){
            checkstatus().then(status=>{
                if(status === false){
                    this.$message.warning("Login expired");
                    this.$store.commit('changeLoginStatus','error');
                }
                else if (status == 'server error'){
                    this.$message.error(status);
                }
                else{
                    this.delete(row);
                }
            }) 
        },
        delete(row)
        {
            var token = getcsrftoken('csrftoken');
            var formdata = new FormData();
            formdata.append('csrfmiddlewaretoken',token);
            formdata.append('file',row['filename']);
            this.axios({
                url: 'api/remove',
                method:'post',
                data:formdata,
                headers :{'Content-Type':'application/x-www-form-urlencoded'}
            }).then(response =>{
                var status = response.data['status'];
                if(status==='delete_ok')
                    this.reloadFlag = !this.reloadFlag;
                else
                    this.$message.warning(status);
            })
            .catch(error =>{
                this.$$message.error("delete request error");
            })
        } 
    }
}
</script>
<style scoped>

</style>