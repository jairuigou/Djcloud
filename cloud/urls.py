from django.urls import path,re_path
from . import views

urlpatterns = [
        path('',views.Index,name='Index'),
        path('verify',views.Verify,name='Verify'),
        path('logout',views.Logout,name='Logout'),
        path('upload',views.Upload,name='Upload'),
        path('delet',views.Delete,name='Delete'),
	re_path(r'^download/$',views.Download,name='Download'),
] 
