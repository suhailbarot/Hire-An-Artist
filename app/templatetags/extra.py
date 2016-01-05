from django import template

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
