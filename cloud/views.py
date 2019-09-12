from django.http import HttpResponse,HttpResponseRedirect,JsonResponse,FileResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import Filepath
import os,datetime,getpass

savePath = "/home/"+getpass.getuser()+"/cloudfile/"
session_time = 100000
root_path = '/'
#views
@ensure_csrf_cookie
def Index(request):
    if request.user.is_authenticated:
        filelist = Filepath.objects.filter(owner = request.user.username)
        context = {
                'username' : request.user.username,
                'fileList' : filelist,
        }
        return render(request,'cloud/clientarea.html',context)
    else:
        return render(request,'cloud/index.html')

def Verify(request):
    data = {
            'status' : 'login_failed'
    }
    if request.user.is_authenticated:
        data['status'] = 'logged'
        return JsonResponse(data)
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username,password=password)
    if user is not None:
        login(request,user)
        data['status'] = 'login_ok'
    return JsonResponse(data)
    
def Logout(request):
    logout(request) 
    return HttpResponseRedirect(root_path)    

def Upload(request):
    data = {
            'status': 'upload_failed',
    }
    if not request.user.is_authenticated:
        data['status'] = 'not_logged'
        return JsonResponse(data)
    uploadfile = request.FILES['file']
    username = request.user.username
    if uploadfile:
        filename = get_filename(uploadfile.name)
        filetype = uploadfile.content_type
        viewtype = get_viewtype(filename)
        savedir = mkdir_foruser(username) 
        fp = open((savedir+filename),"wb")
        for chunk in uploadfile.chunks():
            fp.write(chunk)
        fp.close()
        obj = Filepath(owner=username,filename=filename,filetype=filetype,viewtype=viewtype,uploaddate=datetime.date.today())
        obj.save()
        data['status'] = 'upload_ok'
    return JsonResponse(data)

def Delete(request):
    data = { 
            'status' : 'delete_failed'
    }
    if not request.user.is_authenticated:
        data['status'] = 'not_logged'
        return JsonResponse(data)
    filename = request.POST['file']
    username = request.user.username 
    hasFile = Filepath.objects.filter(filename=filename)
    if hasFile:
        hasFile.delete() 
        rmfile(username,filename)
        data['status'] = 'delele_ok'
    return JsonResponse(data)

def Download(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(root_path) 
    filename = request.GET.get('f')
    username = request.user.username
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

