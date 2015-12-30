from django.conf.urls import include, url
from django.contrib import admin
from app import views
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

    #artist stuff

    url(r'^artist/register/','app.views.artist_register', name='artist_register'),
    url(r'^artist/home/','app.views.artist_home', name='artist_home'),


    #listing stuff

    url(r'listing/add/', 'app.views.add_listing', name='add_listing'),
    url(r'artist/(?P<lid>\w+)/$', 'app.views.view_listing', name='view_listing'),
    url(r'artist/(?P<lid>\w+)/projects/$', 'app.views.view_listing_projects', name='view_projects'),
    url(r'artist/(?P<lid>\w+)/media/manage/$', 'app.views.manage_media', name='manage_media'),
    url(r'artist/(?P<lid>\w+)/media/$', 'app.views.view_media', name='view_media'),
    url(r'artist/(?P<lid>\w+)/edit/$', 'app.views.edit_listing', name='listing_edit'),
    url(r'^search/','app.views.search_home',name='search'),
    url(r'^results/','app.views.search_results',name='search_results'),


    ## media stuff ###for

    url( r'upload/', views.image_upload, name = 'jfu_upload' ),
    url(r'media/(?P<lid>\w+)/images/$', 'app.views.image_view_api', name='img_api'),


    #password and user auth

    url(r'^reset/(?P<key>\w+)/$','app.views.reset_password', name='password_reset'),
    url(r'^forgot/','app.views.forgot_password', name='forgot_pass'),
    url(r'^logout/','app.views.logout_user',name='logout'),
    url(r'', include('social_auth.urls')),
    url(r'^login/','app.views.user_login',name='login'),

    #admin stuff

    url(r'^admin/', include(admin.site.urls))
]
