from django.conf.urls import include, url
from django.contrib import admin
from app import views
urlpatterns = [
    # Examples:
    # url(r'^$', 'amp.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'app.views.home', name='home'),

    #user stuff

    url(r'^user/register/','app.views.user_register', name='user register'),
    url(r'^user/home/','app.views.user_home', name='logged in home user'),
    url(r'^user/phone/','app.views.add_phone', name='add phone'),

    #artist stuff

    url(r'^artist/register/','app.views.artist_register', name='artist register'),
    url(r'^artist/home/','app.views.artist_home', name='logged in home'),


    #listing stuff

    url(r'listing/add/', 'app.views.add_listing', name='add a listing'),
    url(r'artist/(?P<lid>\w+)/$', 'app.views.view_listing', name='view listing'),
    url(r'artist/(?P<lid>\w+)/projects/$', 'app.views.view_listing_projects', name='view projects'),


    #password and user auth

    url(r'^reset/(?P<key>\w+)/$','app.views.reset_password', name='password reset'),
    url(r'^forgot/','app.views.forgot_password', name='forgot pass'),
    url(r'^logout/','app.views.logout_user',name='log out'),
    url(r'', include('social_auth.urls')),
    url(r'^login/','app.views.user_login',name='log in'),

    #admin stuff

    url(r'^admin/', include(admin.site.urls))
]
