from django.http import HttpResponse,HttpResponseRedirect,JsonResponse,FileResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import Filepath

from .func.handlefile import *
import os,datetime,getpass


SESSION_TIME = 100000
# to index page
ROOT_URL = '/'
#views
@ensure_csrf_cookie
def api_verify(request):
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
        request.session.set_expiry(SESSION_TIME)
        data['status'] = 'login_ok'
    return JsonResponse(data) 
@ensure_csrf_cookie
def api_checkstatus(request):
    data = {
        'status':'not_logged'
    }
    if request.user.is_authenticated:
        data['status'] = 'logged'
    return JsonResponse(data)
def api_logout(request):
    data = {
        'status':'not_logged'
    }
    requeststatus = request.POST['status']
    if request.user.is_authenticated:
        logout(request)
        data['status'] = 'logout_ok'
    return JsonResponse(data)
def api_infodata(request):
    data = {
        'status':'not_logged',
    }
    if request.user.is_authenticated:
        data['status'] = 'logged'
        filelist = Filepath.objects.filter(owner=request.user.username)
        for i,li in enumerate(filelist):
            dic = {}
            dic['filename'] = li.filename
            dic['name'] = li.viewname
            dic['size'] = li.viewsize
            dic['type'] = li.viewtype
            dic['date'] = li.uploaddate
            data[i] = dic
    return JsonResponse(data)
def api_upload_smallfile(request):
    data = {
            'status': 'upload_failed',
    }
    if not request.user.is_authenticated:
        data['status'] = 'not_logged'
        return JsonResponse(data)
    uploadfile = request.FILES['file']
    username = request.user.username
    if uploadfile:
        filename = parse_filename(uploadfile.name,Filepath)
        filetype = uploadfile.content_type
        viewtype = parse_viewtype(filename)
        filesize = uploadfile.size
        viewsize = parse_viewsize(filesize)
        viewname = parse_viewname(filename)
        savedir = generate_savepath(username) 
        fp = open((savedir+filename),"wb")
        for chunk in uploadfile.chunks():
            fp.write(chunk)
        fp.close()
        obj = Filepath(owner=username,filename=filename,filetype=filetype,
                        viewtype=viewtype,filesize=filesize,viewsize=viewsize,
                        viewname=viewname,uploaddate=datetime.date.today())
        obj.save()
        data['status'] = 'upload_ok'
    return JsonResponse(data)
def api_remove(request):
    data = { 
            'status' : 'delete_failed'
    }
    if not request.user.is_authenticated:
        data['status'] = 'not_logged'
        return JsonResponse(data)
    filename = request.POST['file']
    username = request.user.username 
    hasFile = Filepath.objects.filter(filename=filename)
    if hasFile and hasFile[0].owner == username:
        hasFile.delete() 
        rm_file(username,filename)
        data['status'] = 'delete_ok'
    return JsonResponse(data)

def api_emit(request):
    if not request.user.is_authenticated:
        return HttpResponse(status_code="502")
    filename = request.POST['file']
    username = request.user.username
    hasFile = Filepath.objects.filter(filename=filename)
    if not hasFile or hasFile[0].owner != username:
        return HttpResponse(status_code="404")
    if not is_hasfile(username,filename):
        return HttpResponse(status_code="404")
    response = FileResponse( open(FILE_SAVE_PATH+username+'/'+filename,'rb') )
    return response

def api_view(request):
    if not request.user.is_authenticated:
        return HttpResponse(status_code="502")
    filename = request.POST['file']
    username = request.user.username
    hasFile = Filepath.objects.filter(filename=filename)
    if not hasFile or hasFile[0].owner != username:
        return HttpResponse(status_code="404")
    if not is_hasfile(username,filename):
        return HttpResponse(status_code="404")
    return HttpResponse( open(FILE_SAVE_PATH+username+'/'+filename,'rb'))
    

def upload_largefile_post(request):
    data = {
        'status':'upload_failed',
    }
    if not request.user.is_authenticated:
        data['status'] = 'not_logged'
        return JsonResponse(data)
    uploadslice = request.FILES['blob']
    username = request.user.username
    if uploadslice:
        filename = request.POST['filename']
        slicesize = uploadslice.size
        totalsize = request.POST['totalsize']
        slicesnum = request.POST['slicesnum']
        filetype = request.POST['type']
        sliceindex = request.POST['index']

        savedir = generate_savepath(username)
        fp = open((savedir+"slice/"+filename+sliceindex),"wb") 
        for chunk in uploadslice.chunks():
            fp.write(chunk)
        fp.close()
        if int(sliceindex) == slicesnum :
            data['status'] = 'upload_ok'
        else:
            data['status'] = 'upload_slice_ok'
    return JsonResponse(data)





