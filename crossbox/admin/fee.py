from django.contrib import admin


class FeeAdmin(admin.ModelAdmin):
    list_display = (
        'label', 'num_sessions', 'price_cents', 'active')
    search_fields = [
        'label', 'num_sessions', 'price_cents', 'active']
    ordering = ['num_sessions', 'price_cents', 'active']

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['num_sessions', 'price_cents']
        else:
            return []

    def has_delete_permission(self, request, obj=None):
        return False
