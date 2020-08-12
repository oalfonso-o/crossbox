from django.contrib import admin


class SubscriberAdmin(admin.ModelAdmin):
    list_display = 'username', 'first_name', 'last_name', 'wods'
    search_fields = [
        'user__first_name', 'user__last_name', 'user__username', 'wods'
    ]
    ordering = ['user', 'wods']
    readonly_fields = ['user', 'stripe_customer_id', 'stripe_subscription_id']

    def has_add_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        return []
