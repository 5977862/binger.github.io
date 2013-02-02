from django.contrib import admin
from news.models import news

class newsAdmin(admin.ModelAdmin):
    list_display = ('title','body')
    search_fields = ('title','body')

admin.site.register(news,newsAdmin)