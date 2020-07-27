from datetime import date, timedelta

from django.contrib import admin

from crossbox.models import Reservation, Session


class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user_info', 'session', 'refund')
    list_editable = ('refund',)
    search_fields = [
        'user__first_name', 'user__last_name', 'user__username']
    ordering = ['user', 'refund']
    list_per_page = 20

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'session':
            queryset = Session.objects.filter(
                date__gte=date.today() - timedelta(days=date.today().weekday())
            ).order_by('date', 'hour__hour')
            kwargs['queryset'] = queryset
        return super(ReservationAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs
        )


class ReservationAdminInline(admin.TabularInline):
    model = Reservation
