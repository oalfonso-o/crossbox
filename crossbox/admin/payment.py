from django.contrib import admin


class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'subscriber',
        'fee',
        'datetime',
        'payed_amount',
        'wods',
        'stripe_error',
    )
    search_fields = [
        'subscriber__pk',
        'subscriber__username',
        'subscriber__first_name',
        'subscriber__last_name',
        'subscriber__email',
        'datetime',
        'payed_amount',
    ]
    ordering = ['datetime']

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False
