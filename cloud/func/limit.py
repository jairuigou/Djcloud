import time

LIMITUA = {'curl','python'}
TIMEKEY= 'timstamp'
INTERVAL = 2
class LimitGate:
    request = None
    def __init__(self,request):
        super().__init__()
        self.request = request 
    def isPass(self):
        flag = self.checkSession() and self.checkHeader()
        self.stamp()
        return flag
    def stamp(self):
        path = self.request.path
        if path == '/verify' or path == '/checkstatus':
            self.request.session[TIMEKEY] = time.time()
    def checkHeader(self):
        UserAgent = self.request.headers['User-Agent']
        for lua in LIMITUA:
            if UserAgent.find(lua) != -1:
                return False
        return True
    def checkSession(self):
        path = self.request.path
        session = self.request.session
        if path == '/verify':
            if TIMEKEY not in session:
                return False
            else:
                lasttime = session[TIMEKEY]
                curtime = time.time()
                if abs(int(curtime) - int(lasttime)) < INTERVAL:
                    return False
        return True