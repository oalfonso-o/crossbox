from django.contrib import admin

from .reservation import ReservationAdminInline


class SessionAdmin(admin.ModelAdmin):
    inlines = (ReservationAdminInline,)
    list_display = ('date', 'hour')
    search_fields = [
        'date', 'hour__hour']
    ordering = ['date', 'hour__hour']
    list_per_page = 20
