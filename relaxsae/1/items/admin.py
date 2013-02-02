from django.contrib import admin
from items.models import Relax,Relax_Relation,JoinUs,Problem,Problem_Relation,Tutsau,Tutsau_Relation

class RelaxAdmin(admin.ModelAdmin):
    list_display = ('username','title','body','date')
    search_fields = ('username__username','title','body')

class JoinUsAdmin(admin.ModelAdmin):
    list_display = ('username','title','date')
    search_fields = ('username__username','title__title')

class ProblemAdmin(admin.ModelAdmin):
    list_display = ('username','title','body','date')
    search_fields = ('username__username','title','body')

class TutsauAdmin(admin.ModelAdmin):
    list_display = ('username','title','body','date')
    search_fields = ('username__username','title','body')

class RelationAdmin(admin.ModelAdmin):
    list_display = ('username','title','text','date')
    search_fields = ('username__username','title__title','text')

admin.site.register(Relax,RelaxAdmin)
admin.site.register(Relax_Relation,RelationAdmin)
admin.site.register(JoinUs,JoinUsAdmin)
admin.site.register(Problem,ProblemAdmin)
admin.site.register(Problem_Relation,RelationAdmin)
admin.site.register(Tutsau,TutsauAdmin)
admin.site.register(Tutsau_Relation,RelationAdmin)