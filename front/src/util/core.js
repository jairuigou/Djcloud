import axios from 'axios'

axios.defaults.baseURL = '/';

async function checkstatus()
{
    try{
        var res = await axios({
        url:'api/checkstatus',
        method:'get',
        headers :{'Content-Type':'application/x-www-form-urlencoded'}
        });
    }
    catch(err){
        return 'server error';
    }
    var status = res.data['status'];
    if(status == 'not_logged')
        return false;
    else
        return true;
}
function getcsrftoken(name)
{
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
export {checkstatus,getcsrftoken};