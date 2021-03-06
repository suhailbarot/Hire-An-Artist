import datetime
import pprint


from django.core.mail import send_mail
from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


from app.forms import RegisterForm,LoginForm,ForgotPasswordForm,PhoneForm, ListingForm, ListingProjectFormSet,HomeSearchForm, ArtistNameSearch, UserProfileEditForm

from app.models import PasswordReset, UserProfile, Listing, Projects, Function, Talent, Tag
from app.utils import generate_hash
from app.constants import VISITOR_ID,ARTIST_ID

# Create your views here.

########### GENERIC ###################


def home(request):
    return HttpResponse("Hello")


def user_login(request):
    if request.POST:
        form = LoginForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            logged_in_user = form.save()
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
        form = LoginForm()
    return render(request,'login.html',{'form':form})


def logout_user(request):
    logout(request)
    return HttpResponse("Logged Out")


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
            print e
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
        form = RegisterForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            new_user = form.save(actype=ARTIST_ID)
            return HttpResponse("done")
    else:
        form = RegisterForm()
    return render(request,'artist_register.html',{'form':form})

@login_required(login_url='/login')
def artist_home(request):
    if request.user.is_authenticated():
        up = UserProfile.objects.get(user=request.user)
        ls = Listing.objects.filter(user=up)
        return render(request,'artist_home.html',{'listings':ls,'up':up})
    return HttpResponse("I don't think we have met before")


#####################      VISTORS         ####################


def user_register(request):
    if request.POST:
        form = RegisterForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            new_user = form.save(actype=VISITOR_ID)
            return HttpResponse("done")
    else:
        form = RegisterForm()
    return render(request,'user_register.html',{'form':form})


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
        formset = ListingProjectFormSet(request.POST)

        if form.is_valid():
            usr = UserProfile.objects.get(user=request.user)
            k = form.save(commit=False)
            formset = ListingProjectFormSet(request.POST, instance=k)
            if formset.is_valid():
                l = form.save(commit=True,user=usr)
                formset.save(commit=True)
                return HttpResponseRedirect(reverse('view_listing',kwargs={'lid':l.id}))
    else:
        form = ListingForm()
        formset = ListingProjectFormSet(instance=Listing())

    return render(request,'add_listing.html',{'form':form,'formset':formset})


def edit_listing(request,lid):
    try:
        listing = Listing.objects.get(id=lid)
    except Listing.DoesNotExist:
        return HttpResponse("WTF")
    if request.POST:
        form = ListingForm(data=request.POST or None, files=request.FILES , instance=listing)
        formset = ListingProjectFormSet(request.POST,instance=listing)
        if form.is_valid():
            usr = UserProfile.objects.get(user=request.user)
            k = form.save(commit=False)
            formset = ListingProjectFormSet(request.POST, instance=k)
            if formset.is_valid():
                l = form.save(commit=True,user=usr)
                formset.save(commit=True)
                return HttpResponseRedirect(reverse('view_listing',kwargs={'lid':l.id}))
    else:
        form = ListingForm(instance=listing)
        formset = ListingProjectFormSet(instance=listing,queryset=Projects.objects.filter(is_active=1))

    return render(request,'edit_listing.html',{'form':form,'formset':formset,'listing':listing})


def view_listing(request,lid):
    try:
        listing = Listing.objects.get(id=lid, is_active=1)
    except Listing.DoesNotExist:
        return HttpResponse("No such listing")
    return render(request,'view_listing.html',{'listing':listing})


def view_listing_projects(request,lid):
    try:
        listing = Listing.objects.get(id=lid, is_active=1)
    except Listing.DoesNotExist:
        return HttpResponse("No such Listing")

    projects = Projects.objects.filter(listing=listing, is_active=1)

    return render(request,"view_listing_projects.html",{'listing':listing,'projects':projects})


######### HOME #########

def search_home(request):
    form = HomeSearchForm()
    artist_search = ArtistNameSearch()
    return render(request, 'home_search.html',{'form':form,'name':artist_search})


def search_results(request):
    if request.POST:
        results = None
        if 'filter_form' in request.POST:
            print request.POST
            results = Listing.objects.filter(is_active=1)

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
        return render(request,"search_results.html",{'result':results})
    return HttpResponseRedirect(reverse('search'))