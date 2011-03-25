from django.contrib import admin

from problem import models as pmodels

def resolve(modeladmin,request,queryset):
	queryset.update(resolved=True)

resolve.short_description = "Mark selected problems as resolved"

class ProblemAdmin(admin.ModelAdmin):
	list_filter = ('resolved',)
	list_display = ('content_object','notes','resolved','user')
	exclude = ('content_type','object_id',)
	actions = [resolve]

admin.site.register(pmodels.ProblemFlag,ProblemAdmin)
