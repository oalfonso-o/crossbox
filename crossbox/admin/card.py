from django.contrib import admin


class CardAdmin(admin.ModelAdmin):
    list_display = ('subscriber', 'last_digits', 'default')
    search_fields = ['subscriber', 'last_digits', 'default']
    ordering = ['subscriber', 'last_digits', 'default']
    readonly_fields = ('subscriber', 'last_digits', 'default')

    def has_add_permission(self, request, obj=None):
        return False
