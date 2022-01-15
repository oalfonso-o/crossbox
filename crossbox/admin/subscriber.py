from django.contrib import admin

from crossbox.models.payment import Payment


class PaymentAdminInline(admin.TabularInline):
    model = Payment

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class SubscriberAdmin(admin.ModelAdmin):
    inlines = (PaymentAdminInline,)
    list_display = (
        'username', 'first_name', 'last_name', 'wods',
        'last_payment_datetime', 'next_billing_cycle_datetime'
    )
    search_fields = [
        'user__first_name', 'user__last_name', 'user__username', 'wods'
    ]
    ordering = ['user', 'wods']
    readonly_fields = ['user']

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
