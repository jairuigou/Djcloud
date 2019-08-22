from django.urls import path,re_path
from . import views

urlpatterns = [
        path('',views.index,name='index'),
        path('verify',views.verify,name='verify'),
        path('logout',views.logout,name='logout'),
        path('upload',views.upload,name='upload'),
        path('delet',views.delet,name='delet'),
		re_path(r'^download/$',views.download,name='download'),
] 
