from django.contrib import admin


class CardAdmin(admin.ModelAdmin):
    list_display = ('subscriber', 'last_digits', 'active')
    search_fields = ['subscriber', 'last_digits', 'active']
    ordering = ['subscriber', 'last_digits', 'active']
    readonly_fields = ('last_digits',)

    def has_add_permission(self, request, obj=None):
        return False
