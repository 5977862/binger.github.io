from django.contrib import admin
from ifoundyou.models import CoordinateTimes,Coordinate

class CoordinateAdmin(admin.ModelAdmin):
    list_display = ('times','telephone','now_time')
    search_fields = ('times',)

class CoordinateTimesAdmin(admin.ModelAdmin):
    list_display = ('times','longitude','latitude')
    search_fields = ('times__times','longitude','latitude')
    
admin.site.register(CoordinateTimes,CoordinateTimesAdmin)
admin.site.register(Coordinate,CoordinateAdmin)