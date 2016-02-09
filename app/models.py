from django.db import models
from django.contrib.auth.models import User

import uuid
import os

def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('profile', filename)

# Create your models here.

class UserProfile(models.Model):
    """
    User model contains what?
    username ***
    first_name
    last_name
    email
    password ***

    To make a new user

    1. Visitor
    FB/Google/Email
    username - fbid,googleid,email
    pass

    2. Artist
    username = email
    pass

    """
    user = models.OneToOneField(User)
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=12, blank=True, null=True)
    type_choice = (
        (1,'Sub Admin'),
        (2, 'Artist'),
        (3, 'Visitor')
    )
    type = models.IntegerField(choices=type_choice, default=3)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_active = models.IntegerField(default=1)

    class Meta:
        app_label = 'app'

    def __unicode__(self):
        return str(self.full_name)

    def __str__(self):
        return str(self.full_name)


class Talent(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    fee_text = models.CharField(max_length=300,blank=True)
    is_active = models.IntegerField(default=1)

    class Meta:
        app_label = 'app'

    def __unicode__(self):
        return str(self.name)

    def __str__(self):
        return str(self.name)


class Function(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_active = models.IntegerField(default=1)

    class Meta:
        app_label = 'app'

    def __unicode__(self):
        return str(self.name)

    def __str__(self):
        return str(self.name)


class Tag(models.Model):
    name = models.CharField(max_length=100)
    talent = models.ForeignKey(Talent)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_active = models.IntegerField(default=1)

    class Meta:
        app_label = 'app'

    def __unicode__(self):
        return str(self.name)

    def __str__(self):
        return str(self.name)


class Listing(models.Model):
    profile_pic = models.ImageField(upload_to=get_file_path,blank=True,verbose_name='Upload your listing picture')
    name = models.CharField(max_length=200,verbose_name="Name your listing *")
    city = models.CharField(max_length=100,verbose_name="Which city are you based out of? *")
    choice = (
        (1,'YES'),
        (2,'NO')
    )
    outstation = models.IntegerField(choices=choice, default=1,verbose_name="Do you provides services outstation? *")
    contact_name = models.CharField(max_length=200,verbose_name='Name of the contact person *')
    contact_email = models.EmailField(default=None, blank=True, null=True, verbose_name='Contact email *')
    contact_number = models.CharField(max_length=12,verbose_name='Contact number *')
    contact_number2 = models.CharField(max_length=12, blank=True, null=True, verbose_name='Additional contact number 1')
    contact_number3 = models.CharField(max_length=12, blank=True, null=True, verbose_name='Additional contact number 2')
    bio = models.CharField(max_length=1000, blank=True)
    fees = models.IntegerField(verbose_name='What are your charges? *')
    comments = models.CharField(max_length=1000, blank=True, null=True, verbose_name="Additional notes for your fees")
    tech_details = models.CharField(max_length=2000, blank=True, null=True)
    tech_details_file = models.FileField(blank=True, null=True, upload_to='tech_det', verbose_name='Additional Detail File')
    fb_link = models.URLField(blank=True, null=True)
    twitter_link = models.URLField(blank=True, null=True)
    user = models.ForeignKey(UserProfile)
    score = models.IntegerField(default=1)
    is_approved = models.IntegerField(default=0)
    talents = models.ForeignKey(Talent,null=True, blank=True) #mandatory
    functions = models.ManyToManyField(Function) #mandatory
    tags = models.ManyToManyField(Tag,blank=True)
    address = models.CharField(max_length=2000,blank=True)
    address_city = models.CharField(max_length=500, blank=True, verbose_name="Locality, City")
    latitude = models.CharField(max_length=100,blank=True)
    longitude = models.CharField(max_length=100,blank=True)
    group_key = models.CharField(max_length=15, blank=True)
    param_1 = models.IntegerField(default=-1)
    param_2 = models.IntegerField(default=-1)
    param_3 = models.IntegerField(default=-1)
    param_4 = models.IntegerField(default=-1)
    param_5 = models.IntegerField(default=-1)
    param_6 = models.IntegerField(default=-1)
    param_7 = models.IntegerField(default=-1)
    param_8 = models.IntegerField(default=-1)
    param_9 = models.IntegerField(default=-1)
    param_10 = models.IntegerField(default=-1)
    rscore = models.DecimalField(max_digits=5,decimal_places=3,default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_active = models.IntegerField(default=1)

    class Meta:
        app_label = 'app'

    def __unicode__(self):
        return str(self.name)


class Projects(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    referral_name = models.CharField(max_length=100,blank=True,null=True)
    referral_email = models.EmailField(blank=True, null=True)
    referral_contact = models.CharField(max_length=12,blank=True,null=True)
    referral_contact_2 = models.CharField(max_length=12, blank=True, null=True)
    listing = models.ForeignKey(Listing)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_active = models.IntegerField(default=1)

    class Meta:
        app_label = 'app'


class Media(models.Model):
    title = models.CharField(max_length=200, blank=True)
    caption = models.CharField(max_length=200, blank=True)
    choices = (
        (1,'Image'),
        (2,'Youtube'),
        (3,'Soundcloud')
    )
    type = models.IntegerField(choices=choices)
    url = models.URLField()
    listing = models.ForeignKey(Listing)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_active = models.IntegerField(default=1)

    class Meta:
        app_label = 'app'

class Review(models.Model):
    content = models.CharField(max_length=2000)
    listing = models.ForeignKey(Listing)
    user = models.ForeignKey(UserProfile)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_active = models.IntegerField(default=1)

    class Meta:
        app_label = 'app'


class Rating(models.Model):
    score = models.IntegerField(default=0)
    listing = models.ForeignKey(Listing)
    user = models.ForeignKey(UserProfile)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_active = models.IntegerField(default=1)

    class Meta:
        app_label = 'app'


class PasswordReset(models.Model):
    key = models.CharField(max_length=200)
    email = models.EmailField()

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_active = models.IntegerField(default=1)

    class Meta:
        app_label = 'app'


class City(models.Model):
    name = models.CharField(max_length=100)
    is_popular = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_active = models.IntegerField(default=1)

    def __unicode__(self):
        return str(self.name)

    class Meta:
        app_label = 'app'
        verbose_name_plural = 'cities'

