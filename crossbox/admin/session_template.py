from django.contrib import admin


class SessionTemplateAdmin(admin.ModelAdmin):
    list_display = (
        'day', 'hour', 'week_template', 'capacity_limit', 'morning')
    search_fields = ['day__name', 'hour__hour']
    ordering = ['day', 'hour__hour', 'week_template__name', 'morning']
