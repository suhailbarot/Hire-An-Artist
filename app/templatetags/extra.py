from django import template
from app.models import UserProfile

register = template.Library()

@register.simple_tag(takes_context=True)
def get_city(context):
    request = context['request']
    result = request.COOKIES.get('city','')
    return result

@register.assignment_tag(takes_context=True)
def cookie_city(context):
    request = context['request']
    result = request.COOKIES.get('city','')
    return result

@register.simple_tag(takes_context=True)
def get_user_name(context):
    request = context['request']
    try:
        up = UserProfile.objects.get(is_active=1,user=request.user)
        return up.full_name
    except:
        pass
    return ""

@register.assignment_tag()
def get_user_type(a):
#    request = context['request']
    try:
        up = UserProfile.objects.get(is_active=1,user=a)
        print up.type
        return up.type

    except:
        pass
    print "wirow"
    return ""

@register.simple_tag()
def get_rating(listing):
    star = '<span class="rating-star %s"></span>'
    avg = 0.0
    cnt = 0
    for x in range(1,11):
        par = "param_"+str(x)
        num = getattr(listing, par)
        print num
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
    return final_c

