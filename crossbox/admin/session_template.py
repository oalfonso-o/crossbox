from django.contrib import admin


class SessionTemplateAdmin(admin.ModelAdmin):
    list_display = ('day', 'hour')
    search_fields = ['day__name', 'hour__hour']
    ordering = ['day', 'hour__hour']
