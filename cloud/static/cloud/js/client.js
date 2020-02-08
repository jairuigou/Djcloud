var upload = new Vue({
    el: '#upload',
    data:{
        file : "",
        totalsize : 0,
        slicesize : 1024*1024*3,
        slicesnum : 0,
        istart : 0,
        iend : 0,
        index : 1,
        retrycount : 0,
    },
    methods:{
        upload:function(){
            this.file = document.getElementById("input_file").files[0]
            if(this.file.size<this.slicesize){
                this.uploadsmallfile()
            }
            else{
                this.uploadlargefile()
            }
        },
        uploadsmallfile: function(){
			let token = this.getcsrftoken('csrftoken') 
            formdata = new FormData()
           	formdata.append('file',this.file)
            formdata.append('csrfmiddlewaretoken',token) 
            axios({
            	url: 'uploadsmall',
            	method:'post',
                data:formdata,
                headers: {'Content-Type': 'application/x-www-form-urlencoded'},
                onUploadProgress: progressEvent=>{
                    var percentCompleted = Math.round( (progressEvent.loaded * 100) / progressEvent.total )
                    document.getElementById("result").innerHTML = percentCompleted + '%'
                }
            }).then(response => {
            	var status = response.data['status']
            	if(status == "upload_ok"){
            		document.getElementById("result").innerHTML += "  upload success"
					location.reload(true)
            	}
           		else if(status == "upload_failed"){
                	document.getElementById("result").innerHTML += "  upload failed" 
            	}
            	else{
                	location.reload(true)
            	}
            })
              .catch(error=>{
                    console.log(error)
                    document.getElementById("result").innerHTML = "  smallfile upload response error"  
              })
       
        },
        uploadlargefile:function(){
            this.totalsize = this.file.size
            this.slicesnum = Math.ceil(this.totalsize / this.slicesize)
            this.loopajax()
        },
        loopajax:function(){
            if(this.istart>=this.totalsize){
	            document.getElementById("result").innerHTML += "  upload error"
                return
            }
            this.iend = this.istart + this.slicesize
            if(this.iend> this.totalsize)
                this.iend = this.totalsize
            let slice = this.file.slice(this.istart,this.iend)
            let token = this.getcsrftoken('csrftoken')
            formdata = new FormData()
            formdata.append('filename',this.file.name)
            formdata.append('type',this.file.type)
            formdata.append('totalsize',this.totalsize)
            formdata.append('slicesnum',this.slicesnum)
            formdata.append('index',this.index++)
            formdata.append('csrfmiddlewaretoken',token)
            formdata.append('blob',slice)
            axios({
                url:'uploadlarge',
                method:'post',
                data: formdata,
                headers: {'Content-Type': 'application/x-www-form-urlencoded'},
            }).then(response=>{
                var status = response.data['status']
                if(status == "upload_failed"){
                    if(this.retrycount < 3){
                        this.loopajax()
                        this.retrycount++
                    }
                    else{
                        this.istart = this.iend
                        this.loopajax()
                    }
                }
                else if(status == "upload_slice_ok"){
                    this.istart = this.iend
                    this.loopajax()
                }
                else if(status == "upload_ok"){
	                document.getElementById("result").innerHTML += "  upload success"
                }
            }).catch(error=>{
	                document.getElementById("result").innerHTML += "  largefile upload response error"
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
		remove: function(item){
            var intext = item.currentTarget.parentNode.innerText
            let filename = intext.split(' ') 
            let token = upload.getcsrftoken('csrftoken')
            formdata = new FormData()
            formdata.append('file',filename[0])
            formdata.append('csrfmiddlewaretoken',token) 
            axios({
                   url: 'remove',
                   method:'post',
                   data:formdata,
                   headers: {'Content-Type': 'application/x-www-form-urlencoded'}
            }).then(response => {
                    var status = response.data['status']
                    if(status== "delete_ok"){
						document.getElementById("result").innerHTML += "  delete success"
						location.reload(true)
					}
                    else if(status=="delete_failed"){
						document.getElementById("result").innerHTML += "  delete failed" 
					}
                    else {
						location.reload(true)
					}
            })
            .catch(error=>{
				   	document.getElementById("result").innerHTML += "  delete response error " 
            })
		},
		download:function(item){
			var intext = item.currentTarget.parentNode.innerText
			let filename = intext.split(' ')
			location.href='/download/?f='+filename[0]	
		},
    }

})
