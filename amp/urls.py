from django.conf.urls import include, url
from django.contrib import admin
from app import views
from django.views.generic import TemplateView
urlpatterns = [
    # Examples:
    # url(r'^$', 'amp.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'app.views.home', name='home'),

    #user stuff

    url(r'^user/register/','app.views.user_register', name='user_register'),
    url(r'^user/home/','app.views.user_home', name='user_home'),
    url(r'^user/phone/','app.views.add_phone', name='add_phone'),
    url(r'^account/update/','app.views.edit_profile', name='edit_profile'),
    url(r'^account/password/','django.contrib.auth.views.password_change',
        {'template_name': 'change_password.html'},
        name='password_change_done'),
    url(r'^user/login','app.views.user_login',name = 'user_login'),

    #artist stuff

    url(r'^artist/register/','app.views.artist_register', name='artist_register'),
    url(r'^artist/home/','app.views.artist_home', name='artist_home'),


    #listing stuff

    url(r'listing/add/', 'app.views.add_listing', name='add_listing'),
    url(r'artist/(?P<lid>\w+)/$', 'app.views.view_listing', name='view_listing'),
    url(r'artist/(?P<lid>\w+)/projects/$', 'app.views.view_listing_projects', name='view_projects'),
    url(r'artist/(?P<lid>\w+)/media/manage/$', 'app.views.manage_media', name='manage_media'),
    url(r'artist/(?P<lid>\w+)/media/$', 'app.views.view_media', name='view_media'),
    url(r'artist/(?P<lid>\w+)/uploads/$', 'app.views.edit_uploads', name='edit_uploads'),
    url(r'artist/(?P<lid>\w+)/edit/$', 'app.views.edit_listing', name='listing_edit'),
    url(r'^search/','app.views.search_home',name='search'),
    url(r'^results/','app.views.search_results',name='search_results'),
    url(r'base/',TemplateView.as_view(template_name='root/base.html')),


    ## media stuff ###for

    url( r'media/upload/', views.image_upload, name='jfu_upload'),
    url( r'^media/delete/(?P<pk>\d+)$', views.upload_delete, name='jfu_delete'),
    url( r'^media/image_update/$', views.image_update, name='image_update'),
    url( r'^video_audio/add/$', views.video_audio_add, name='video_add'),
    url( r'^video/update/$', views.video_update, name='video_update'),
    url( r'^sound/update/$', views.sound_update, name='sound_update'),
    url( r'^video_audio/delete/$', views.youtube_soundcloud_delete, name='yt_sc_delete'),
    url(r'media/(?P<lid>\w+)/images/$', 'app.views.image_view_api', name='img_api'),



    #password and user auth

    url(r'^reset/(?P<key>\w+)/$','app.views.reset_password', name='password_reset'),
    url(r'^forgot/','app.views.forgot_password', name='forgot_pass'),
    url(r'^logout/','app.views.logout_user',name='logout'),
    url(r'', include('social_auth.urls')),
    url(r'^login/','app.views.user_login',name='login'),

    #admin stuff

    url(r'^admin/', include(admin.site.urls)),

    ## helper stuff

    url(r'^api/city_list/$','app.api.handlers.city_list', name='city_list'),
    url(r'^set_city/$','app.api.handlers.set_city', name='set_city'),
    url(r'^api/listing_name/$','app.api.handlers.get_listing_autocomplete', name='listing_autocomplete')

]
