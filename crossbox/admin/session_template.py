from django.contrib import admin

from crossbox.models.session import Session


class SessionTemplateAdmin(admin.ModelAdmin):
    list_display = ('day', 'hour', 'week_template', 'capacity_limit')
    search_fields = ['day__name', 'hour__hour']
    ordering = ['day', 'hour__hour', 'week_template__name']
