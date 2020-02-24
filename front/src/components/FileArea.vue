<template>
    <el-container>
        <el-container>
        <el-aside width="110px"> 
            <el-row type="flex" justify="center">
                <el-avatar shape="circle" icon="el-icon-user" :size="70"></el-avatar>
            </el-row>
            <el-row class="toptoucharea">
                <el-row type="flex" justify="center" align="middle">
                <i class="el-icon-upload2"></i>
                </el-row>
                <el-row type="flex" justify="center">
                <el-button type="text" class="textbutton">upload</el-button>
                </el-row>
            </el-row>
            <el-row class="middletoucharea" >
                <el-row type="flex" justify="center" align="middle">
                <i class="el-icon-picture-outline"></i>
                </el-row>
                <el-row type="flex" justify="center">
                <el-button type="text" class="textbutton">picture</el-button>
                </el-row>
            </el-row>
            <el-row class="middletoucharea" >
                <el-row type="flex" justify="center" align="middle">
                <i class="el-icon-document"></i>
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
            <el-row class="bottomtoucharea" >
                <el-row type="flex" justify="center" align="middle">
                <i class="el-icon-refresh"></i>
                </el-row>
                <el-row type="flex" justify="center">
                <el-button type="text" class="textbutton" @click="changestatus()">refresh</el-button>
                </el-row>
            </el-row>
        </el-aside>
        </el-container>
        <el-container>
        <el-header>
            <el-input 
                placeholder="search" 
                suffix-icon="el-icon-search" 
                clearable
                class="searchinput"
            ></el-input>
        </el-header>
        <el-main>
            <el-table
            :data="tableData">
                <el-table-column label="filename" prop="name">
                </el-table-column>
                <el-table-column label="filetype" prop="type">
                </el-table-column>
                <el-table-column label="filesize" prop="size">
                </el-table-column>
                <el-table-column label="date" prop="date">
                </el-table-column>
            </el-table>
        </el-main>
        </el-container>
    </el-container>    
</template>
<script>
export default {
    data(){
        return{
            reloadFlag:false,
            tableData:[]
        }
    },
    watch:{
        reloadFlag:function() {
            this.axios({
                url:'api/infodata',
                method: 'get',
            }).then(response =>{
                var status = response.data['status'];
                if(status == "not_logged"){
                    alert("not logged");
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
    font-size: 40px;
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
    font-size: 40px;
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
    font-size: 40px;
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