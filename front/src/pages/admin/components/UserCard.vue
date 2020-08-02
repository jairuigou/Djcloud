<template>
    <el-card shadow="hover" class = "usercard" :body-style="{ padding: '0px'}">
        <div v-if="hasInfo == true">
            <img id="avatarimg" src="../../../assets/3.jpg" class="image">
            <div style="padding : 10px">
                <span >{{info.UserName}}</span>
                <div class="greencircle" v-if="info.Status=='online'"></div>
                <div v-if="info.Status!='online'">{{info.LastLoginTime}}</div>
                <el-progress class="usage" :stroke-width="10" :show-text="false" 
                    :percentage="info.DiskUsage/info.DiskAllocation*100"></el-progress>
            </div>
        </div>
        <div v-else>
            add an user
        </div>
    </el-card>
</template>
<script>
export default {
    data(){
        return{
            hasInfo: true,
            info:{
                'UserName':'jairui',
                'Status':'online',
                'LastLoginTime':'2020/05/05',
                'DiskUsage':'10',
                'DiskAllocation':'20',
                'AvatarLink':'None'
            }
        }
    },
    mounted:function(){
        if(info.AvatarLink != "None"){
            var obj = document.
        }
    },
    methods:{

    }
    
}
</script>
<style scoped>
.el-icon-plus{
    font-size: 150px;
}
.image{
    width:100%;
    height:180px;
    display: block;
}
.usercard{
    width:200px;
    height: 250px;
    border-radius: 3%;
}
.greencircle{
    margin: 8px;
    display:inline-block;
    width:6px;
    height:6px;
    background: #67C23A;
    border-radius: 50%;
}
.usage{
    margin-top: 10px;
    margin-bottom: 10px;
}

</style>