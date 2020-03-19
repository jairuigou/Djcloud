from django.urls import path,re_path
from . import views

urlpatterns = [
        path('uploadlarge',views.upload_largefile_post,name='upload_largefile_post'),
        

        path('uploadsmall',views.api_upload_smallfile,name='api_upload_smallfile'),
        path('verify',views.api_verify,name='api_verify'),
        path('infodata',views.api_infodata,name="api_infodata"),
        path('checkstatus',views.api_checkstatus,name ='api_checkstatus'),
        path('logout',views.api_logout,name='api_logout'),
        path('remove',views.api_remove,name='api_remove'),
        path('download',views.api_emit,name='api_emit'),
        path('view',views.api_view,name='api_view')
] 
