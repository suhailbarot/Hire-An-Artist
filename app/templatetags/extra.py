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

@register.simple_tag(takes_context=True)
def get_user_type(context):
    request = context['request']
    try:
        up = UserProfile.objects.get(is_active=1,user=request.user)
        return up.type

    except:
        pass
    return ""