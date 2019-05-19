from django.contrib import admin


class HourAdmin(admin.ModelAdmin):
    list_display = ('hour_range',)
    search_fields = ['hour']
    ordering = ['hour']
