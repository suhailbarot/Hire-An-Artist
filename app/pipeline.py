import pprint
from social_auth.backends.facebook import FacebookBackend

from django.http import HttpResponse

from app.models import UserProfile
from app.constants import VISITOR_ID



def create_user_profile(*args, **kwargs):
    # if not strategy.session_get('saved_username') and kwargs['user'] is None:
    # return HttpResponse("Hello")
    # else:
    # pprint.pprint(kwargs['user'])
    #     return None
    if 'user' in kwargs and kwargs['user']:
        usr = kwargs['user']
        if kwargs['backend'].__class__ == FacebookBackend:
            usr.first_name = str(kwargs['response'][u'name'])
            usr.save()
        try:
            old = UserProfile.objects.get(user=usr)
        except UserProfile.DoesNotExist:
            uc = UserProfile.objects.create(user=usr, full_name=str(usr.first_name) + " " + str(usr.last_name),
                                            email=usr.email, type=VISITOR_ID)
    return None
