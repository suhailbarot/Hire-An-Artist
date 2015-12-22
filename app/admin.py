from django.contrib import admin
from app.models import *
# Register your models here.

admin.site.site_header = 'HireTheArtist Admin'

class ProjectInline(admin.TabularInline):
    model = Projects
    extra = 1

class MediaInline(admin.TabularInline):
    model = Media
    extra = 1

class ListingAdmin(admin.ModelAdmin):
    inlines = [ProjectInline, MediaInline]

admin.site.register(Listing, ListingAdmin)
admin.site.register(UserProfile)
admin.site.register(Review)
admin.site.register(Rating)
admin.site.register(Media)
admin.site.register(PasswordReset)
admin.site.register(Talent)
admin.site.register(Function)
admin.site.register(Tag)