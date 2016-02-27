import datetime
from PIL import Image
from StringIO import StringIO
from jfu.http import upload_receive, UploadResponse, JFUResponse
import time
import boto
import json
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder



from django.views.decorators.http import require_POST
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from endless_pagination.decorators import page_template
from django.template import RequestContext
from django.core.mail import send_mail
from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login,authenticate
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core import serializers



from django.conf import settings
from app.forms import RegisterForm,LoginForm,ForgotPasswordForm,PhoneForm, ListingForm, \
    ListingProjectFormSet,HomeSearchForm, ArtistNameSearch, UserProfileEditForm,\
    FilterSearchForm,HomeArtistNameSearch, ProfilePicForm, AdditionalForm,RatingForm

from app.models import PasswordReset, UserProfile, Listing, Projects, Function, Talent, Tag, Media, City
from app.utils import generate_hash
from app.constants import VISITOR_ID,ARTIST_ID, VIDEO, SOUND, PHOTO
from app.utils import video_id

# Create your views here.

########### GENERIC ###################


def home(request):
    artist_form = HomeArtistNameSearch()
    form = HomeSearchForm()
    cities = City.objects.filter(is_active=1,is_popular=1).order_by('name')
    if request.POST:
        if "register" in request.POST:
            form1 = RegisterForm(data=request.POST, files=request.FILES)
            form2=LoginForm()
            if form1.is_valid():
                new_user = form1.save(actype=ARTIST_ID)
                new_use = authenticate(username=request.POST['email'],
                                    password=request.POST['password1'])
                login(request, new_use)
                return HttpResponse("done")
        elif "login" in request.POST:
            form2 = LoginForm(data=request.POST)
            form1=RegisterForm()
            if form2.is_valid():
                logged_in_user = form2.save()
                if logged_in_user.is_active == 1:
                    login(request, logged_in_user)
                    up = UserProfile.objects.get(user=logged_in_user)
                    if up.type == VISITOR_ID:
                        return HttpResponseRedirect(reverse('user_home'))
                    else:
                        return HttpResponseRedirect(reverse('artist_home'))
                else:
                    return HttpResponse("Not active")
    else:
        form1 = RegisterForm()
        form2 = LoginForm()

    return render(request,'home_page.html',{'form':form,'artist_form':artist_form,'cities':cities,'form_login':form2,'form_register':form1})


def user_login(request):
    redirect_to = request.POST.get('next', '')

    if request.POST:
        form = LoginForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            logged_in_user = form.save()
            if logged_in_user.is_active == 1:
                login(request, logged_in_user)
                up = UserProfile.objects.get(user=logged_in_user)
                if up.type == VISITOR_ID:
                    return HttpResponseRedirect(reverse(redirect_to))
                else:
                    return HttpResponseRedirect(reverse(redirect_to))
            else:
                return HttpResponse("Not active")
    else:
        form = LoginForm()
    return render(request,'login.html',{'form':form})


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))


def reset_password(request, key):
    if key:
        dt = datetime.datetime.now() - datetime.timedelta(hours=1)
        try:
            pr = PasswordReset.objects.filter(key=key, created_at__gte=dt, is_active=1).order_by('created_at')[0]
            usr = User.objects.get(username__iexact=pr.email)
            new_p = generate_hash(pr.email)[:8]
            usr.set_password(new_p)
            usr.save()
            message = "Your new password is "+str(new_p)
            pr.is_active=0
            pr.save()
            # send_mail("Reset your password",message,'support@bla.com',[pr.email], fail_silently=True)
            return HttpResponse("A new password has been emailed to you :" + message)
        except Exception,e:
            return HttpResponse("Invalid Attempt")


def forgot_password(request):
    if request.user.is_authenticated():
        return HttpResponse("Already Logged in")
    if request.POST:
        form = ForgotPasswordForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.complete()
            return HttpResponse("Check your mail for a link bruh")
    else:
        form = ForgotPasswordForm()
    return render(request,'forgot_password.html',{'form':form})




def edit_profile(request):
    if request.user.is_authenticated():
        up = UserProfile.objects.get(user=request.user)
        form = UserProfileEditForm(request.POST or None,instance=up)
        if request.POST:
            if 'basic' in request.POST:
                if form.is_valid():
                    form.save()
                    return HttpResponseRedirect(reverse('edit_profile'))
        return render(request,'edit_profile.html',{'form':form})
    return HttpResponse("Not Authorized")

#####################      ARTISTS        ####################


def artist_register(request):
    if request.POST:
        if "register" in request.POST:
            form1 = RegisterForm(data=request.POST, files=request.FILES)
            form2=LoginForm()
            if form1.is_valid():
                new_user = form1.save(actype=ARTIST_ID)
                new_use = authenticate(username=request.POST['email'],
                                    password=request.POST['password1'])
                login(request, new_use)
                return HttpResponse("done")
        elif "login" in request.POST:
            form2 = LoginForm(data=request.POST)
            form1=RegisterForm()
            if form2.is_valid():
                logged_in_user = form2.save()
                if logged_in_user.is_active == 1:
                    login(request, logged_in_user)
                    up = UserProfile.objects.get(user=logged_in_user)
                    if up.type == VISITOR_ID:
                        return HttpResponseRedirect(reverse('user_home'))
                    else:
                        return HttpResponseRedirect(reverse('artist_home'))
                else:
                    return HttpResponse("Not active")
    else:
        form1 = RegisterForm()
        form2 = LoginForm()
    return render(request,'artist_register.html',{'form_register':form1,'form_login':form2})


@login_required(login_url='/login')
def artist_home(request):
    if request.user.is_authenticated():
        up = UserProfile.objects.get(user=request.user)
        ls = Listing.objects.filter(is_active=1,user=up)
        return render(request,'artist_home.html',{'listings':ls,'up':up})
    return HttpResponse("I don't think we have met before")


#####################      VISTORS         ####################


def user_register(request):
    redirect_to = request.REQUEST.get('next', '')

    if request.POST:
        form = RegisterForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            new_user = form.save(actype=VISITOR_ID)
            new_use = authenticate(username=request.POST['email'],
                                    password=request.POST['password1'])
            login(request, new_use)

            return HttpResponseRedirect(redirect_to)
    else:
        form = RegisterForm()
    return render(request,'user_register.html',{'form':form})

def user_login(request):
    redirect_to = request.REQUEST.get('next', '')
    if request.POST:
        form = LoginForm(data=request.POST)
        if form.is_valid():
            logged_in_user = form.save()
            if logged_in_user.is_active == 1:
                login(request, logged_in_user)
                up = UserProfile.objects.get(user=logged_in_user)
                if up.type == VISITOR_ID:
                    return HttpResponseRedirect(redirect_to)
                else:
                    return HttpResponseRedirect(redirect_to)
            else:
                return HttpResponse("Not active")
    else:
        form = LoginForm()
    return render(request,'user_login.html',{'form_login':form})



def user_home(request):
    if request.user.is_authenticated():
        return HttpResponse("Hi"+str(request.user.email))
    return HttpResponse("Chllies")


def add_phone(request):
    if request.user.is_authenticated():
        usp = UserProfile.objects.get(user=request.user)
        if request.POST:
            form = PhoneForm(data=request.POST)
            if form.is_valid():
                form.save(usp)
                return HttpResponseRedirect(reverse('user_home'))
        else:
            form = PhoneForm()
        return render(request,'enter_phone.html',{'form':form})





####### LISTING #########


def add_listing(request):
    if request.POST:
        form = ListingForm(data=request.POST, files=request.FILES)
        # formset = ListingProjectFormSet(request.POST)
        if form.is_valid():
            usr = UserProfile.objects.get(user=request.user)
            l = form.save(commit=True,user=usr)
            # im = Image.open(form.cleaned_data['profile_pic'])
            # box=(int(form.cleaned_data['x']),int(form.cleaned_data['y']),int(form.cleaned_data['x'])+int(form.cleaned_data['x2']),int(form.cleaned_data['y2'])+int(form.cleaned_data['y']))
            # im2 = im.crop(box)
            # img_io = StringIO()
            # im2.save(img_io, format='JPEG')
            # img_content = InMemoryUploadedFile(img_io, None, 'foo.jpg', 'image/jpeg',
            #                       img_io.len, None)
            # k = form.save(commit=False)
            # k.profile_pic = img_content
            # formset = ListingProjectFormSet(request.POST, instance=k)
            # if formset.is_valid():
            #     l = form.save(commit=True,user=usr)
                # formset.save(commit=True)
            return HttpResponseRedirect(reverse('edit_uploads',kwargs={'lid':l.id}))
    else:
        usr = UserProfile.objects.get(user=request.user)
        form = ListingForm(initial={'contact_name':usr.full_name,'contact_number':usr.phone,'contact_email':usr.email})
        # formset = ListingProjectFormSet(instance=Listing())

    return render(request,'add_listing.html',{'form':form})


def edit_listing(request,lid):
    try:
        listing = Listing.objects.get(id=lid)
    except Listing.DoesNotExist:
        return HttpResponse("WTF")
    if request.POST:
        form = ListingForm(data=request.POST or None, files=request.FILES , instance=listing)
        if form.is_valid():
            usr = UserProfile.objects.get(user=request.user)
            l = form.save(commit=True,user=usr)
            return HttpResponseRedirect(reverse('view_listing',kwargs={'lid':l.id}))
    else:
        form = ListingForm(instance=listing)

    return render(request,'add_listing.html',{'form':form,'listing':listing})


def view_listing(request,lid):
    phoneform = PhoneForm()

    try:
        listing = Listing.objects.get(id=lid, is_active=1)
        rating_form = RatingForm(instance=listing)
        media = Media.objects.filter(is_active=1, listing=listing)
        projects = Projects.objects.filter(listing=listing, is_active=1)
        if listing.group_key:
            similar = Listing.objects.filter(group_key=listing.group_key).exclude(id=listing.id)
        else:
            similar = []
        yt = []
        sc = []
        ph = []
        for media in media:
            if media.type == PHOTO:
                ph.append(media)
            if media.type == VIDEO:
                vd = video_id(media.url)
                media.vid = vd
                yt.append(media)
            if media.type == SOUND:
                sc.append(media)
    except Listing.DoesNotExist:
        return HttpResponse("No such listing")
    if request.POST:
        if "rate" in request.POST:
            form1 = RegisterForm()
            form2=LoginForm()
            listing = Listing.objects.get(id=lid, is_active=1)
            rating_form = RatingForm(data=request.POST,instance=listing)
            if rating_form.is_valid():
                rated = rating_form.save()
            return render(request,'view_listing.html',{'listing':listing,'videos':yt[:4],'sounds':sc,
                                               'images':ph[:4],'image_count':max(0,len(ph)-4),
                                               'video_count':max(0,len(yt)-4),'projects':projects,'similar':similar,'phoneform':phoneform,'form_login':form2,'form_register':form1,'rating_form':rating_form})

        if "register" in request.POST:
            form1 = RegisterForm(data=request.POST, files=request.FILES)
            form2=LoginForm()
            if form1.is_valid():
                new_user = form1.save(actype=ARTIST_ID)
                new_use = authenticate(username=request.POST['email'],
                                    password=request.POST['password1'])
                login(request, new_use)
                return HttpResponse("done")
        elif "login" in request.POST:
            form2 = LoginForm(data=request.POST)
            form1=RegisterForm()
            if form2.is_valid():
                logged_in_user = form2.save()
                if logged_in_user.is_active == 1:
                    login(request, logged_in_user)
                    up = UserProfile.objects.get(user=logged_in_user)
                    if up.type == VISITOR_ID:
                        return HttpResponseRedirect(reverse('user_home'))
                    else:
                        return HttpResponseRedirect(reverse('artist_home'))
                else:
                    return HttpResponse("Not active")
    else:
        form1 = RegisterForm()
        form2 = LoginForm()

    return render(request,'view_listing.html',{'listing':listing,'videos':yt[:4],'sounds':sc,
                                               'images':ph[:4],'image_count':max(0,len(ph)-4),
                                               'video_count':max(0,len(yt)-4),'projects':projects,'similar':similar,'phoneform':phoneform,'form_login':form2,'form_register':form1,'rating_form':rating_form})


def view_listing_projects(request,lid):
    try:
        listing = Listing.objects.get(id=lid, is_active=1)
    except Listing.DoesNotExist:
        return HttpResponse("No such Listing")
    projects = Projects.objects.filter(listing=listing, is_active=1)
    return render(request,"view_listing_projects.html",{'listing':listing,'projects':projects})


def edit_uploads(request, lid):
    try:
        listing = Listing.objects.get(id=lid, is_active=1, user__user=request.user)
    except Listing.DoesNotExist:
        return HttpResponse("No such listing")
    pf = ProfilePicForm(instance=listing)
    af = AdditionalForm(instance=listing)
    af_vis = False
    pf_vis = False
    md = Media.objects.filter(is_active=1, listing=listing)
    yt = []
    sc = []
    ph = []
    for media in md:
        if media.type == PHOTO:
            ph.append(media)
        if media.type == VIDEO:
            vd = video_id(media.url)
            media.vid = vd
            yt.append(media)
        if media.type == SOUND:
            sc.append(media)
    if request.POST:
        if 'profile_pic_form' in request.POST:
            pf = ProfilePicForm(data = request.POST, files=request.FILES, instance=listing)
            if pf.is_valid():
                pf.save()
            else:
                pf_vis = True
        if 'additional_form' in request.POST:
            af = AdditionalForm(data=request.POST, files=request.FILES, instance=listing)
            if af.is_valid():
                af.save()
            else:
                af_vis = True
    return render(request,'edit_uploads.html',{'listing':listing,'pf':pf,'af':af,'af_vis':af_vis,'pf_vis':pf_vis,
                                               'sounds':sc,'videos':yt,'images':ph,
                                               'VIDEO':VIDEO,'SOUND':SOUND,'PHOTO':PHOTO})


##### MEDIA STUFF #########

def view_media(request,lid):
    try:
        listing = Listing.objects.get(id=lid,is_active=1)
    except Listing.DoesNotExist:
        return HttpResponse("No such Listing")
    md = Media.objects.filter(is_active=1, listing=listing)
    yt = []
    sc = []
    ph = []
    for media in md:
        if media.type == PHOTO:
            ph.append(media)
        if media.type == VIDEO:
            vd = video_id(media.url)
            media.vid = vd
            yt.append(media)
        if media.type == SOUND:
            sc.append(media)
    return render(request,'view_media.html',{'videos':yt,'sounds':sc,'images':ph})


def manage_media(request,lid):
    try:
        listing = Listing.objects.get(id=lid,is_active=1)
    except Listing.DoesNotExist:
        return HttpResponse("Hi")
    md = Media.objects.filter(is_active=1, listing=listing)
    yt = []
    sc = []
    ph = []
    for media in md:
        if media.type == PHOTO:
            ph.append(media)
        if media.type == VIDEO:
            vd = video_id(media.url)
            media.vid = vd
            yt.append(media)
        if media.type == SOUND:
            sc.append(media)
    return render(request,"manage_media.html",{'listing':listing,'sounds':sc,'videos':yt,'images':ph,
                                               'VIDEO':VIDEO,'SOUND':SOUND,'PHOTO':PHOTO})


@require_POST
def image_upload(request):
    file = upload_receive(request)
    lid = request.POST.get('listing')
    file_type = file.content_type.split('/')[0]
    error = None
    if not file:
        return HttpResponse(status=400)
    try:
        if len(file.name.split('.')) == 1:
            error = "File type not supported. Only JPEG,JPG,PNG and GIF are allowed."
        if file.content_type.split('/')[1] in settings.TASK_UPLOAD_FILE_TYPES:
            if file._size > settings.TASK_UPLOAD_FILE_MAX_SIZE:
                error = "File size over limit. Image must be below 10MB"
        else:
            error = "File type not supported. Only JPEG,JPG,PNG and GIF are allowed"
    except:
        pass
    try:
        usp = UserProfile.objects.get(user=request.user,is_active=1)
        listing = Listing.objects.get(is_active=1,pk=int(lid),user=usp)
    except Listing.DoesNotExist:
        return HttpResponse("Listing does not exist",status=400)

    if error:
        file_dict = {
        'error': error,
        'name' : file.name,
        'size' : file.size
    }
    else:
        timestamp = str(int(time.time()))
        fn = generate_hash(timestamp+str(file.name))
        connection = boto.connect_s3(settings.AWS_ACCESS_KEY_ID,settings.AWS_SECRET_ACCESS_KEY)
        bucket = connection.get_bucket('imgmed')
        key = bucket.new_key('user_data/'+fn+"."+file.content_type.split('/')[1])
        key.set_metadata('Content-Type', file.content_type)
        key.set_contents_from_file(file)
        key.make_public()
        url = key.generate_url(expires_in=0, query_auth=False, force_http=True)

        md = Media.objects.create(listing=listing,url=url,type=PHOTO)
        file_dict = {
            'name' : file.name,
            'size' : file.size,
            'url': url,
            'thumbnailUrl': url,
            'deleteUrl': reverse('jfu_delete', kwargs = { 'pk': md.pk }),
            'deleteType': 'POST',
        }
    return UploadResponse(request,file_dict)


@require_POST
def upload_delete(request,pk):
    success = True
    try:
        md = Media.objects.get(is_active=1,pk=pk)
        connection = boto.connect_s3(settings.AWS_ACCESS_KEY_ID,settings.AWS_SECRET_ACCESS_KEY)
        md.url = md.url.replace("http://", "")
        md.url = md.url.replace("https://", "")
        rest = md.url.split("/")[1:]
        if len(rest) == 0:
            success = False
        else:
            vxs = '/'.join(md.url.split("/")[1:])
            bucket = connection.get_bucket('imgmed')
            bucket.delete_key(vxs)
            md.delete()
    except Media.DoesNotExist:
        success = False
    return JFUResponse(request,success)


@require_POST
def image_update(request):
    mid = request.POST.get('mid')
    title = request.POST.get('title')
    caption = request.POST.get('caption')
    try:
        usp = UserProfile.objects.get(user=request.user,is_active=1)
        md = Media.objects.get(is_active=1,listing__user=usp,pk=mid)
    except:
        error = "Media object does not exist."
        response = {'error':error}
        return HttpResponse(json.dumps(response),status=400)
    md.title = title
    md.caption = caption
    md.save()
    return HttpResponse(json.dumps({'success':'true'}))


@require_POST
def video_audio_add(request):
    listing = request.POST.get('listing')
    link = request.POST.get('link')
    title = request.POST.get('title')
    caption = request.POST.get('caption')
    type = request.POST.get('type')
    try:
        usp = UserProfile.objects.get(is_active=1,user=request.user)
        listing = Listing.objects.get(is_active=1,pk=int(listing),user=usp)
        md = Media.objects.create(url=link,title=title,caption=caption,type=type,listing=listing)
    except:
        return HttpResponse(json.dumps({'error':'unable to add video'}), status=400)
    return HttpResponse(json.dumps({'success':'true'}))


@require_POST
def video_update(request):
    mid = request.POST.get('mid')
    title = request.POST.get('title')
    caption = request.POST.get('caption')
    try:
        usp = UserProfile.objects.get(is_active=1,user=request.user)
        md = Media.objects.get(is_active=1,pk=int(mid),listing__user=usp)
    except:
        return HttpResponse(json.dumps({'error':'unable to modify video'}), status=400)
    md.title = title
    md.caption = caption
    md.save()
    return HttpResponse(json.dumps({'success':'true'}))

@require_POST
def sound_update(request):
    mid = request.POST.get('mid')
    title = request.POST.get('title')
    caption = request.POST.get('caption')
    try:
        usp = UserProfile.objects.get(is_active=1,user=request.user)
        md = Media.objects.get(is_active=1,pk=int(mid),listing__user=usp)
    except:
        return HttpResponse(json.dumps({'error':'unable to modify sound'}), status=400)
    md.title = title
    md.caption = caption
    md.save()
    return HttpResponse(json.dumps({'success':'true'}))

@require_POST
def youtube_soundcloud_delete(request):
    mid = request.POST.get('mid')
    try:
        usp = UserProfile.objects.get(is_active=1,user=request.user)
        md = Media.objects.get(is_active=1,pk=mid,listing__user=usp)
        md.delete()
    except:
        return HttpResponse(json.dumps({'error':'unable to delete video'}), status=400)
    return HttpResponse(json.dumps({'success':'true'}))

def image_view_api(request,lid):
    try:
        listing = Listing.objects.filter(is_active=1,id=lid)
    except Listing.DoesNotExist:
        return HttpResponse("No such artist name")
    photos = Media.objects.filter(is_active=1,listing=listing,type=PHOTO)
    serialized_obj = serializers.serialize('json', photos)
    return HttpResponse(serialized_obj)



######### HOME #########



@page_template('search_results_page.html')  
def search_home(request, template='home_search.html', extra_context=None):
    filter_form = FilterSearchForm(request.GET)
    results = Listing.objects.all()
    cities = City.objects.filter(is_active=1,is_popular=1).order_by('name')


    tn=None

    if request.POST:
        results = None
        if 'filter_form' in request.POST:
            results = Listing.objects.filter(is_active=1)
            if 'filter_by' in request.POST:
                if request.POST['filter_by']==0:
                    results=results.order_by('-fees')



            if 'function_type' in request.POST:
                function = None
                if request.POST['function_type']:
                    function = int(request.POST['function_type'])
                    fn = Function.objects.get(id=function)
                    results = results.filter(functions=fn)

            if 'talents' in request.POST:
                tn = None
                if request.POST['talents']:
                    talents = int(request.POST['talents']) #list of talents
                    tn = Talent.objects.get(id=talents)
                    results = results.filter(talents=tn)


            if 'budget_min' in request.POST:
                if request.POST['budget_min']:
                    budget_min = int(request.POST['budget_min']) #string
                    results = results.filter(fees__gte=budget_min)

            if 'budget_max' in request.POST:
                if request.POST['budget_max']:
                    budget_max = int(request.POST['budget_max'])
                    results = results.filter(fees_lte=budget_max)

            if 'outstation' in request.POST:
                results = results.filter(outstation=True)
            else:
                if 'city' in request.POST:
                    city = None
                    if request.POST['city']:
                        city = request.POST['city'] #string
                        results = results.filter(city__icontains=str(city))

        elif 'name_form' in request.POST:
            results = Listing.objects.filter(is_active=1, name__icontains=str(request.POST['name'].strip()))
    if request.GET: 
        results = Listing.objects.filter(is_active=1)
        if 'filter_form' in request.GET:

            results = Listing.objects.filter(is_active=1)

        


   

        if request.GET.get('function_type'):
            function = int(request.GET['function_type'])
            fn = Function.objects.get(id=function)
            results = results.filter(functions=fn)
        if request.GET.get('talents'):
            talents = int(request.GET['talents']) 
            tn = Talent.objects.get(id=talents)
            results = results.filter(talents=tn)

        if request.GET.get('budget_min'):
            budget_min = int(request.GET['budget_min'])
            results = results.filter(fees__gte=budget_min)
        if request.GET.get('budget_max'):
            budget_max = int(request.GET['budget_max'])
            results = results.filter(fees__lte=budget_max)
        if request.GET.get('city'):
            city = request.GET['city'] 
            results = results.filter(city__icontains=str(city))
        if request.GET.get('outstation'):
            results = results.filter(outstation=True)
        if request.GET.get('filter_by'):
            if int(request.GET['filter_by']) == 0:
                results=results.order_by('fees')

            if int(request.GET['filter_by'])==1:

                for res in results:
                    m=0   
                    sum1=0
                    if res.param_1!=-1:
                        sum1+=res.param_1
                        m+=1
                    if res.param_2!=-1:
                        sum1+=res.param_2
                        m+=1

                    if res.param_3!=-1:
                        sum1+=res.param_3
                        m+=1
                    if res.param_4!=-1:
                        sum1+=res.param_4
                        m+=1
                    if res.param_5!=-1:
                        sum1+=res.param_5
                        m+=1
                    if res.param_6!=-1:
                        sum1+=res.param_6
                        m+=1
                    if res.param_7!=-1:
                        sum1+=res.param_7
                        m+=1
                    if res.param_8!=-1:
                        sum1+=res.param_8
                        m+=1
                    if res.param_9!=-1:
                        sum1+=res.param_9
                        m+=1
                    if res.param_10!=-1:
                        sum1+=res.param_10
                        m+=1
                    if request.GET.get('talents'):
                        tagss = res.tags.filter(talent=int(request.GET['talents']))
                        n=0
                        for tag in tagss:
                            if 'tags' in request.GET:
                                if str(tag.pk) in request.GET['tags']:
                                    sum1+=10
                                    n+=1
                    else:
                        n=0
                    if (m+n)==0:
                        res.rscore = float(0)
                    else:
                        res.rscore=sum1/float(m+n)
                    
                results=sorted(results,key=lambda a: a.rscore,reverse=True)


    if tn:
        context = {'results':results,'form':filter_form,'tn':tn,'cities':cities}
    else:
        context = {'results':results,'form':filter_form,'cities':cities}

    if extra_context is not None:
        context.update(extra_context)

    for listing in results:
        listing.tag_names = listing.tags.all()




    return render_to_response(
        template, context, context_instance=RequestContext(request))



def ajax(request):

    if request.is_ajax():
        usp = UserProfile.objects.get(user=request.user)

        if request.GET:
            


               
            


            if usp.phone:
                l = request.GET.get('listing')
                listing = Listing.objects.get(name=l)
                message = {}
                message['phone'] = 1
                message['latit'] = listing.latitude
                message['longit'] = listing.longitude
                message['contact_name'] = listing.contact_name
                message['contact_number'] = listing.contact_number
                message['address_city'] = listing.address_city
                return JsonResponse({'message':message})


            else:
                message = {}
                message['phone'] = 0
                return JsonResponse({'message':message})
        

        if request.POST:
            message = {}
            form = PhoneForm(data=request.POST)
            if not isinstance(int(form.data['phone']),(int,long)):
                message['status'] = 3
                return JsonResponse({'message': message})
            if len(str(form.data['phone']))<10 or len(str(form.data['phone']))>12:
                message['status'] = 2
                return JsonResponse({'message': message})


            if form.is_valid():
                
                form.save(usp)

                message['status'] = 1 
                return JsonResponse({'message': message})
            else:
            	message['failiure'] = "form not valid"
            return HttpResponse(json.dumps({'message': message}))
        



    return render_to_response(
        template, context, context_instance=RequestContext(request))


def ajaxforfilters(request):
    if request.is_ajax():
        if request.GET:

            if request.GET:

                results = Listing.objects.filter(is_active=1)

        


   

                if request.GET.get('function_type'):
                    function = int(request.GET['function_type'])
                    fn = Function.objects.get(id=function)
                    results = results.filter(functions=fn)
                if request.GET.get('talents'):
                    talents = int(request.GET['talents']) 
                    tn = Talent.objects.get(id=talents)
                    results = results.filter(talents=tn)

                if request.GET.get('budget_min'):
                    budget_min = int(request.GET['budget_min'])
                    results = results.filter(fees__gte=budget_min)
                if request.GET.get('budget_max'):
                    budget_max = int(request.GET['budget_max'])
                    results = results.filter(fees__lte=budget_max)
                if request.GET.get('city'):
                    city = request.GET['city'] 
                    results = results.filter(city__icontains=str(city))
                if request.GET.get('outstation'):
                    results = results.filter(outstation=True)
                if request.GET.get('filter_by'):
                    if int(request.GET['filter_by']) == 0:
                        results=results.order_by('fees')

                    if int(request.GET['filter_by'])==1:

                        for res in results:
                            m=0   
                            sum1=0
                            if res.param_1!=-1:
                                sum1+=res.param_1
                                m+=1
                            if res.param_2!=-1:
                                sum1+=res.param_2
                                m+=1

                            if res.param_3!=-1:
                                sum1+=res.param_3
                                m+=1
                            if res.param_4!=-1:
                                sum1+=res.param_4
                                m+=1
                            if res.param_5!=-1:
                                sum1+=res.param_5
                                m+=1
                            if res.param_6!=-1:
                                sum1+=res.param_6
                                m+=1
                            if res.param_7!=-1:
                                sum1+=res.param_7
                                m+=1
                            if res.param_8!=-1:
                                sum1+=res.param_8
                                m+=1
                            if res.param_9!=-1:
                                sum1+=res.param_9
                                m+=1
                            if res.param_10!=-1:
                                sum1+=res.param_10
                                m+=1
                            if request.GET.get('talents'):
                                tagss = res.tags.filter(talent=int(request.GET['talents']))
                                n=0
                                for tag in tagss:
                                    if 'tags' in request.GET:
                                        if str(tag.pk) in request.GET['tags']:
                                            sum1+=10
                                            n+=1
                            else:
                                n=0
                            if (m+n)==0:
                                res.rscore = float(0)
                            else:
                                res.rscore=sum1/float(m+n)
                    
                        results=sorted(results,key=lambda a: a.rscore,reverse=True)
            message = """"""
            for res in results:
                star = '<span class="rating-star %s"></span>'
                avg = 0.0
                cnt = 0
                for x in range(1,11):
                    par = "param_"+str(x)
                    num = getattr(res, par)
                    if num > 0:
                        avg += num
                        cnt += 1
                if cnt>0:
                    avg /= cnt
                avg/=2.0
                full_star = int(avg)
                half_star = 1 if (avg-full_star) >= 0.5 else 0
                final_c = ""
                tot = 5
                for j in range(full_star):
                    final_c+=star % "full-star"
                    tot-=1
                for j in range(half_star):
                    final_c+=star % "half-star"
                    tot-=1
                for j in range(tot):
                    final_c+=star % "empty-star"
                    

                tagstring=""""""
                count=0
                for t in res.tags.all():
                    if count>=4:
                        break
                    count+=1
                    tagstring+="""
                                                    
                                                    <p class="tag">

                                                        %s
                                                    </p>
                                                    
                                                    
                                                """%(t)
                mess = """<div class="col-md-6">

                        <div class="content-box">
                            <div class="result-card">
                                <div class="row">
                                        <div class="col-md-4">
                                            <img src="listing.profile_pic" class="card-image">
                                        </div>

                                        <div class="col-md-8 listing-card-data">
                                            <div class="row">
                                                <div class="col-md-12">
                                            <div class="rating rating-box">
                                             %s 
                                        </div>
                                        </div>


                                            <div class="col-md-12">

                                    <div class="listing-name">
                                        <h5>%s</h5>
                                    </div>
                                                <div class="listing-talent">
                                                    <h6>%s</h6>
                                                </div>
                                                <div class="listing-tags">

                                                %s
                                                </div>


                                                <div class="listing-price">
                                                  %s
                                                </div>
                                                </div>
                                            </div>

                                    </div>
                            </div>

</div>
                    </div>
                        </div>"""%(final_c,res.name,res.talents,tagstring,res.fees)
                message+=mess

 
            return HttpResponse(message)
