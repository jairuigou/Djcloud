from django.http import HttpResponse,HttpResponseRedirect,JsonResponse,FileResponse
from django.shortcuts import render
from django.urls import reverse
from .models import User,Filepath
from django.views.decorators.csrf import ensure_csrf_cookie
import os,datetime,getpass

savePath = "/home/"+getpass.getuser()+"/cloudfile/"
session_time = 100000
root_path = '/'
#views
@ensure_csrf_cookie
def index(request):
    if is_logged(request):
        fileList = Filepath.objects.filter(username=request.session['username'])
        context = {
                'username' : request.session['username'],
                'fileList' : fileList,
        }
        return render(request,'cloud/clientarea.html',context)
    else:
        return render(request,'cloud/index.html')

def verify(request):
    username = request.POST['username']
    passwd = request.POST['password']
    hasUser = User.objects.filter(username=username)
    data = {
            'status' : 'login_failed' ,
            }
    if hasUser:
        if(hasUser[0].passwd == passwd):
            if is_logged(request):
                data['status'] = 'logged'
            else:
                request.session['username'] = hasUser[0].username
                request.session.set_expiry(session_time)
                data['status'] = 'login_ok'
    return JsonResponse(data) 

def logout(request):
    try:
        del request.session['username']
    except KeyError:
        pass
    return HttpResponseRedirect(root_path)    

def upload(request):
    data = {
            'status': 'upload_failed',
    }
    if not is_logged(request):
        data['status'] = 'not_logged'
        return JsonResponse(data)
    uploadfile = request.FILES['file']
    username = request.session['username']
    if uploadfile:
        filename = get_filename(uploadfile.name)
        filetype = uploadfile.content_type
        viewtype = get_viewtype(filename)
        savedir = mkdir_foruser(username) 
        fp = open((savedir+filename),"wb")
        for chunk in uploadfile.chunks():
            fp.write(chunk)
        fp.close()
        obj = Filepath(username=username,filename=filename,filetype=filetype,viewtype=viewtype,uploaddate=datetime.date.today())
        obj.save()
        data['status'] = 'upload_ok'
    return JsonResponse(data)

def delet(request):
    data = { 
            'status' : 'delete_failed'
    }
    if not is_logged(request):
        data['status'] = 'not_logged'
        return JsonResponse(data)
    dfilename = request.POST['file']
    username = request.session['username'] 
    hasFile = Filepath.objects.filter(filename=dfilename)
    if hasFile:
        hasFile.delete() 
        rmfile(username,dfilename)
        data['status'] = 'delele_ok'
        return JsonResponse(data)
    return JsonResponse(data)

def download(request):
	if not is_logged(request):
		return HttpResponseRedirect(root_path) 
	filename = request.GET.get('f')
	username = request.session['username']
	hasFile = Filepath.objects.filter(filename=filename)
	if hasFile:
		filetype = hasFile[0].filetype
		if(is_hasfile(username,filename)):
			returnfile = open(savePath+username+'/'+filename,'rb').read()
			response = HttpResponse(returnfile,content_type=filetype)
			response['Content-Disposition'] = 'attachment;filename='+filename
			return response
	return HttpResponseRedirect(root_path)
#fun
def mkdir_foruser(username):
    if(not os.path.exists(savePath)):
        os.mkdir(savePath)
    if(not os.path.exists(savePath+ username)):
        os.mkdir(savePath + username)
    return savePath+username+"/"

def rmdir_foruser(username):
    if(os.path.exists(savePath + username)):
        os.rmdir(savePath + username)

def rmfile(username,filename):
    filepath = savePath + username + '/' + filename
    if(os.path.exists(filepath)):
        os.remove(filepath)

def is_hasfile(username,filename):
	filepath = savePath + username + '/' + filename
	if(os.path.exists(filepath)):
		return True
	else:
		return False

def is_logged(request):
    if('username' not in request.session):
        return False
    else:
        return True

def get_viewtype(filename):
	if '.' in filename:
		return filename.split('.')[1]
	else:
		return "unknown"

def get_filename(filename):
    hasFile = Filepath.objects.filter(filename=filename)
    if hasFile:
        if '.' in filename:
            div = filename.split('.',1)
            firstname = div[0]
            secondname = div[1]
            suffix = 0
            while hasFile:
                filename = firstname + "-" + str(suffix) + "." + secondname
                hasFile = Filepath.objects.filter(filename=filename)
                suffix = suffix + 1
        else:
            suffix = 0
            while hasFile:
                filename = filename + "-" + str(suffix)
                hasFile = Filepath.objects.filter(filepath=filename)
                suffix = suffix + 1
    return filename

