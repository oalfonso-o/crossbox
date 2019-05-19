from django.contrib import admin


class DayAdmin(admin.ModelAdmin):
    list_display = ('name', 'weekday')
    search_fields = ['name', 'weekday']
    ordering = ['name', 'weekday']
