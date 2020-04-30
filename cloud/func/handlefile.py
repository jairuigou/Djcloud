import os,datetime,getpass
FILE_SAVE_PATH = "/home/"+getpass.getuser()+"/cloudfile/"

#fun
# get user file path /rootpath/username
def is_userfilepathexist(username):
    return os.path.exists(FILE_SAVE_PATH + username)
def generate_savepath(username):
    if not is_userfilepathexist(username):
        if not os.path.exists(FILE_SAVE_PATH):
            init_total_space()
        init_user_space(username)
    return FILE_SAVE_PATH+username+"/"
def init_total_space():
    os.mkdir(FILE_SAVE_PATH)
def init_user_space(username):
    os.mkdir(FILE_SAVE_PATH + username)
    os.mkdir(FILE_SAVE_PATH + username+"/"+"slice")
def get_space_used(username):
    if is_userfilepathexist(username):
        path = FILE_SAVE_PATH + username
        usedspace = 0
        for root, dirs, files in os.walk(path):
            for name in files:
                filename = os.path.join(root,name)
                usedspace += os.path.getsize(filename)
        return usedspace
    else:
        return 0
    

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

