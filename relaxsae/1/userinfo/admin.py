from django.contrib import admin
from userinfo.models import Userinfo

class UserinfoAdmin(admin.ModelAdmin):
    list_display = ('username','gender','email','telephone','activity','verify','address')
    search_fields = ('username','gender','email','telephone','activity','verify','address')

admin.site.register(Userinfo,UserinfoAdmin)