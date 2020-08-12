from django.contrib import admin


class FeeAdmin(admin.ModelAdmin):
    list_display = (
        'num_sessions', 'price_cents', 'stripe_product_id', 'active')
    search_fields = [
        'num_sessions', 'price_cents', 'stripe_product_id', 'active']
    ordering = ['num_sessions', 'price_cents', 'stripe_product_id', 'active']

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['num_sessions', 'price_cents', 'stripe_product_id']
        else:
            return ['stripe_product_id']
