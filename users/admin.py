from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    filter_horizontal = ('following',)

admin.site.register(Profile, ProfileAdmin)
