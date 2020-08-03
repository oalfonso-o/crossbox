from django.contrib import admin


class WeekTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'default')
    search_fields = ['name', 'default']
    ordering = ['name', 'default']
