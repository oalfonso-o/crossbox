from django.contrib import admin


class CapacityLimitAdmin(admin.ModelAdmin):
    list_display = ('minimum', 'maximum', 'default')
    search_fields = ['minimum', 'maximum', 'default']
    ordering = ['minimum', 'maximum', 'default']
