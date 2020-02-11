from django.urls import path,re_path
from . import views

urlpatterns = [
        path('',views.index_test,name='index_test'),
        path('verify',views.verify_ajax,name='verify_ajax'),
        path('logout',views.logout_get,name='logout_get'),
        path('uploadsmall',views.upload_smallfile_post,name='upload_smallfile_post'),
        path('uploadlarge',views.upload_largefile_post,name='upload_largefile_post'),
        path('remove',views.remove_post,name='remove_post'),
	re_path(r'^download/$',views.download_get,name='download_get'),
] 
