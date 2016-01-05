import json

from django.http import HttpResponse,HttpResponseRedirect

from app.models import City


def city_list(request):
    cities = City.objects.filter(is_active=1).values_list('name',flat=True)
    cities = [s.capitalize() for s in cities]
    return HttpResponse("var cityList = "+json.dumps(list(cities))+";")


def set_city(request):
    city = request.GET.get('city')
    goto = request.GET.get('next')
    if not goto:
        goto = '/'
    max_age = 365 * 24 * 60 * 60
    response = HttpResponseRedirect(goto)
    response.set_cookie('city',str(city),expires=max_age)
    return response