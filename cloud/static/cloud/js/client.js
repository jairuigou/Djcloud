var upload = new Vue({
    el: '#upload',
    data:{
        filepath : "",
        message : "", 
    },
    methods:{
        upload: function(){
            this.filepath = this.$refs.filepath.value
			var file = document.getElementById("input_file").files[0]
            document.getElementById("result").innerHTML = file.name
			let token = this.getcsrftoken('csrftoken') 
            formdata = new FormData()
           	formdata.append('file',file)
            formdata.append('csrfmiddlewaretoken',token) 
            axios({
            	url: 'upload',
            	method:'post',
            	data:formdata,
            	headers: {'Content-Type': 'application/x-www-form-urlencoded'}
            }).then(response => {
            	var fetch = response.data['fetch']
            	if(fetch == "up_suc"){
            		document.getElementById("result").innerHTML += "  upload success"
					location.reload(true)
            	}
           		else if( fetch == "up_fad"){
                	document.getElementById("result").innerHTML += "  upload failed" 
            	}
            	else{
                	location.reload(true)
            	}
            })
              .catch(error=>{
                    document.getElementById("result").innerHTML = "  upload error"  
              })
       
		},
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

    }
})
var filelist = new Vue({
    el:"#filelist",
    data:{
		message : "" ,        
    },
    methods:{
		delet: function(item){
            var intext = item.currentTarget.parentNode.innerText
            let filename = intext.split(' ') 
            let token = upload.getcsrftoken('csrftoken')
            formdata = new FormData()
            formdata.append('file',filename[0])
            formdata.append('csrfmiddlewaretoken',token) 
            axios({
                   url: 'delet',
                   method:'post',
                   data:formdata,
                   headers: {'Content-Type': 'application/x-www-form-urlencoded'}
            }).then(response => {
                    var data = response.data['state']
                    if(data== "log_err"){
                        location.reload(true)
					}
                    else if(data=="del_suc"){
						location.reload(true)
						document.getElementById("result").innerHTML += "  delete success" 
					}
                    else {
						document.getElementById("result").innerHTML += "  delete failed" 
					}
            })
            .catch(error=>{
				   	document.getElementById("result").innerHTML += "  delete error " 
            })
		},
		download:function(item){
			var intext = item.currentTarget.parentNode.innerText
			let filename = intext.split(' ')
			location.href='/cloud/download/?f='+filename[0]	
		},
    }

})
