<template>
    <el-card shadow="hover" class = "usercard" :body-style="{ padding: '0px' }">
        <!--<i class ="el-icon-plus"></i>-->
        <img src="../../../assets/3.jpg" class = "image">
        <div>UserName</div>
    </el-card>    
</template>
<script>
export default {
    
}
</script>
<style scoped>
.el-icon-plus{
    font-size: 150px;
}
.image{
    width: 100%;
    display: block;
}
.usercard{
    width:200px;
    height: 230px;
}
</style>