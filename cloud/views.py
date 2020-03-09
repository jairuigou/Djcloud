from django.http import HttpResponse,HttpResponseRedirect,JsonResponse,FileResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import Filepath
from .forms import LoginForm
import os,datetime,getpass

FILE_SAVE_PATH = "/home/"+getpass.getuser()+"/cloudfile/"
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
            dic['name'] = li.viewname
            dic['size'] = li.viewsize
            dic['type'] = li.viewtype
            dic['date'] = li.uploaddate
            data[i] = dic
    return JsonResponse(data)

def index_test(request):
    if request.user.is_authenticated:
        filelist = Filepath.objects.filter(owner = request.user.username)
        context = {
                'username' : request.user.username,
                'fileList' : filelist,
        }
        return render(request,'cloud/clientarea.html',context)
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            formdata = form.cleaned_data
            user = authenticate(username=formdata['username'],
                                password=formdata['password'])
            if user is not None:
                login(request,user)
                request.session.set_expiry(SESSION_TIME)
                filelist = Filepath.objects.filter(owner = request.user.username)
                context = {
                    'username' : request.user.username,
                    'fileList' : filelist,
                }
                return render(request,'cloud/clientarea.html',context)               
            else:
                return render(request,'cloud/index.html',{'form':form})
    else:
        form = LoginForm()
        return render(request,'cloud/index.html',{'form':form})
   
def index_get(request):
    if request.user.is_authenticated:
        filelist = Filepath.objects.filter(owner = request.user.username)
        context = {
                'username' : request.user.username,
                'fileList' : filelist,
        }
        return render(request,'cloud/clientarea.html',context)
    else:
        return render(request,'dist/index.html')

def verify_ajax(request):
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
    
def logout_get(request):
    logout(request) 
    return HttpResponseRedirect(ROOT_URL)    

def upload_smallfile_post(request):
    data = {
            'status': 'upload_failed',
    }
    if not request.user.is_authenticated:
        data['status'] = 'not_logged'
        return JsonResponse(data)
    uploadfile = request.FILES['file']
    username = request.user.username
    if uploadfile:
        filename = parse_filename(uploadfile.name)
        filetype = uploadfile.content_type
        viewtype = parse_viewtype(filename)
        filesize = uploadfile.size
        viewsize = parse_viewsize(filesize)
        viewname = parse_viewname(filename)
        savedir = get_user_filepath(username) 
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

        savedir = get_user_filepath(username)
        fp = open((savedir+"slice/"+filename+sliceindex),"wb") 
        for chunk in uploadslice.chunks():
            fp.write(chunk)
        fp.close()
        if int(sliceindex) == slicesnum :
            data['status'] = 'upload_ok'
        else:
            data['status'] = 'upload_slice_ok'
    return JsonResponse(data)

def remove_post(request):
    data = { 
            'status' : 'delete_failed'
    }
    if not request.user.is_authenticated:
        data['status'] = 'not_logged'
        return JsonResponse(data)
    filename = request.POST['file']
    username = request.user.username 
    hasFile = Filepath.objects.filter(viewname=filename)
    if hasFile:
        hasFile.delete() 
        rm_file(username,filename)
        data['status'] = 'delete_ok'
    return JsonResponse(data)

def download_get(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(ROOT_URL) 
    filename = request.GET.get('f')
    username = request.user.username
    hasFile = Filepath.objects.filter(filename=filename)
    if hasFile:
        filetype = hasFile[0].filetype
        if(is_hasfile(username,filename)):
            returnfile = open(FILE_SAVE_PATH+username+'/'+filename,'rb').read()
            response = HttpResponse(returnfile,content_type=filetype)
            response['Content-Disposition'] = 'attachment;filename='+filename
            return response
    return HttpResponseRedirect(ROOT_URL)


#fun
# get user file path /rootpath/username
def get_user_filepath(username):
    if(not os.path.exists(FILE_SAVE_PATH + username)):
        if(not os.path.exists(FILE_SAVE_PATH)):
            init_total_space()
        init_user_space(username)
    return FILE_SAVE_PATH+username+"/"
def init_total_space():
    os.mkdir(FILE_SAVE_PATH)
def init_user_space(username):
    os.mkdir(FILE_SAVE_PATH + username)
    os.mkdir(FILE_SAVE_PATH + username+"/"+"slice")

def rm_user_dir(username):
    if(os.path.exists(FILE_SAVE_PATH + username)):
        os.rmdir(FILE_SAVE_PATH + username)

def rm_file(username,filename):
    filepath = FILE_SAVE_PATH + username + '/' + filename
    if(os.path.exists(filepath)):
        os.remove(filepath)

def is_hasfile(username,filename):
	filepath = FILE_SAVE_PATH + username + '/' + filename
	if(os.path.exists(filepath)):
		return True
	else:
		return False

def parse_viewtype(filename):
	if '.' in filename:
		return filename.split('.')[1]
	else:
		return "unknown"

def parse_viewsize(filesize):
    filesizeval = int(filesize)
    B = filesizeval
    count = 0
    while B>1024 :
        B = int(B/1024)
        count += 1
    unit = ['B','KB','MB','GB','TB']
    integer = B
    decimal = int(filesizeval % (pow(1024,count)) / pow(1024,count) * 100)
    viewsize = str(integer) + '.'
    if decimal < 10:
        viewsize += '0'
    viewsize += str(decimal) + unit[count]
    return viewsize

def parse_viewname(filename):
    viewname = filename
    if '.' in filename:
        viewname = filename.split('.',1)[0]
    return viewname

def parse_filename(filename):
    hasFile = Filepath.objects.filter(filename=filename)
    if hasFile:
        if '.' in filename:
            div = filename.split('.',1)
            firstname = div[0]
            secondname = div[1]
            suffix = 0
            while hasFile:
                filename = firstname + "(" + str(suffix) + ")." + secondname
                hasFile = Filepath.objects.filter(filename=filename)
                suffix = suffix + 1
        else:
            suffix = 0
            while hasFile:
                filename = filename + "(" + str(suffix) +")"
                hasFile = Filepath.objects.filter(filename=filename)
                suffix = suffix + 1
    return filename

