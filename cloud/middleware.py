import time

INTERVAL = 1
class BlockFrequentRequestMiddleware:
    def __init__(self,get_response):
        self.get_response = get_response
    
    def __call__(self,request):
        if 'frequent' in request.session:
            lasttime = request.session['frequent']
            print(int(lasttime))
            print(int(time.time()))
            if(int(time.time())-int(lasttime)) < INTERVAL:
                print("blocking=======")
            else:
                print("normal=========")
        print("---------------") 
        request.session['frequent'] = time.time()
        return self.get_response(request)