from django.http import HttpResponse
from .func.limit import LimitGate
class BlockFrequentRequestMiddleware:
    def __init__(self,get_response):
        self.get_response = get_response
    
    def __call__(self,request):
        if not LimitGate(request).isPass():
            return HttpResponse(status='404')
        return self.get_response(request)