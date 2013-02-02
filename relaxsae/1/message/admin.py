from django.contrib import admin
from message.models import Message

class MessageAdmin(admin.ModelAdmin):
    list_display = ('title','body','state','date','user_from','user_to')
    search_fields = ('title','body','state','user_from__username','user_to__username')

admin.site.register(Message,MessageAdmin)