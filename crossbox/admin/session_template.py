from django.contrib import admin


class SessionTemplateAdmin(admin.ModelAdmin):
    list_display = ('day', 'hour')
    search_fields = ['day__name', 'hour__hour']
    ordering = ['day', 'hour__hour']


class WeekTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'default')
    search_fields = ['name', 'default']
    ordering = ['name', 'default']


class AppraisalLimitAdmin(admin.ModelAdmin):
    list_display = ('minimum', 'maximum', 'default')
    search_fields = ['minimum', 'maximum', 'default']
    ordering = ['minimum', 'maximum', 'default']
