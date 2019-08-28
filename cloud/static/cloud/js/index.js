new Vue({
    el: '#login',
    data:{
        username : "",
        password : "",
        message : "",
    },
    methods:{
        getcsrftoken: function(name){
            if(document.cookie && document.cookie!=''){
                var cookies = document.cookie.split(';')
                for( var i=0;i<cookies.length;i++){
                    var cookie = cookies[i]
                    var kk = cookie.split('=')
                    if( kk[0] == name){
                        return kk[1]
                    }
                } 
            }
            return ""
        },
        sendkv: function(){
            this.username = this.$refs.inputname.value
            this.password = this.$refs.inputpass.value
            var csrftoken = this.getcsrftoken('csrftoken')
            var dat = Qs.stringify({
                username: this.username,
                password: this.password,
                csrfmiddlewaretoken: csrftoken
            })
            axios.post("verify",dat,{headers:{'Content-Type':'application/x-www-form-urlencoded'}})
            .then(response => {
                var status = response.data['status']
                if(status == "login_ok" || status == "logged"){
                    location.reload(true)
                }
                else{
                    this.message = "verification failed" 
                }
            })
            .catch(error=>{
                this.message = "verify response error"
            }) 
        }
    }
})

