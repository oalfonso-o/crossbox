from django.contrib import admin


class SessionTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'default')
    search_fields = ['name', 'default']
    ordering = ['-default', 'name']
