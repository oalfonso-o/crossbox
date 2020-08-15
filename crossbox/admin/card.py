from django.contrib import admin


class CardAdmin(admin.ModelAdmin):
    list_display = ('subscriber', 'last_digits', 'default', 'stripe_card_id')
    search_fields = ['subscriber', 'last_digits', 'default', 'stripe_card_id']
    ordering = ['subscriber', 'last_digits', 'default', 'stripe_card_id']
    readonly_fields = (
        'subscriber', 'last_digits', 'default', 'stripe_card_id')

    def has_add_permission(self, request, obj=None):
        return False
