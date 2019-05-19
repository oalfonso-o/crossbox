from django.contrib import admin

from crossbox.models import Reservation


class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user_info', 'session', 'assisted')
    list_editable = ('assisted',)
    search_fields = [
        'user__first_name', 'user__last_name', 'user__username']
    ordering = ['user', 'assisted']
    list_per_page = 20


class ReservationAdminInline(admin.TabularInline):
    model = Reservation
