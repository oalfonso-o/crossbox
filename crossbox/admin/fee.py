from django.contrib import admin


class FeeAdmin(admin.ModelAdmin):
    list_display = (
        'label', 'num_sessions', 'price_cents', 'stripe_product_id', 'active')
    search_fields = [
        'label', 'num_sessions', 'price_cents', 'stripe_product_id', 'active']
    ordering = ['num_sessions', 'price_cents', 'stripe_product_id', 'active']

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return [
                'num_sessions', 'price_cents', 'stripe_product_id',
                'stripe_price_id']
        else:
            return ['stripe_product_id', 'stripe_price_id']

    def has_delete_permission(self, request, obj=None):
        return False
