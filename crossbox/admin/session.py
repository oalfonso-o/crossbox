import datetime

from django.contrib import admin

from .reservation import ReservationAdminInline


class SessionAdminFilter(admin.SimpleListFilter):
    title = 'Por defecto: A partir de esta semana'
    parameter_name = 'filter'

    def lookups(self, request, model_admin):
        return (
            (None, 'A partir de esta semana'),
            ('past', 'Anteriores a esta semana'),
            ('all_desc', 'Todas (primero las últimas)'),
            ('all_asc', 'Todas (primero las primeras)'),
        )

    def queryset(self, request, queryset):
        last_monday = (
            datetime.date.today()
            - datetime.timedelta(
                days=datetime.date.today().weekday()
            )
        )
        if self.value() is None:
            return queryset.filter(date__gte=last_monday).order_by(
                'date', 'hour__hour')
        elif self.value() == 'past':
            return queryset.filter(date__lt=last_monday).order_by(
                '-date', '-hour__hour')
        elif self.value() == 'all_desc':
            return queryset.order_by('-date', '-hour__hour')
        elif self.value() == 'all_asc':
            return queryset.order_by('date', 'hour__hour')


def refund_and_delete(modeladmin, request, queryset):
    for session in queryset:
        for reservation in session.reservations.all():
            reservation.user.subscriber.wods += 1
            reservation.user.subscriber.save()
        session.delete()


refund_and_delete.short_description = (
    'Eliminar sesiones seleccionadas y devolver wods')


class SessionAdmin(admin.ModelAdmin):
    inlines = (ReservationAdminInline,)
    list_filter = (SessionAdminFilter,)
    list_display = ('date', 'hour', 'capacity_limit', 'morning')
    search_fields = ['date', 'hour__hour']
    list_per_page = 20
    actions = [refund_and_delete]
