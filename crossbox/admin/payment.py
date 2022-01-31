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
        'subscriber__user__username',
        'subscriber__user__first_name',
        'subscriber__user__last_name',
        'subscriber__user__email',
        'datetime',
        'payed_amount',
    ]
    ordering = ['-datetime']

    def has_change_permission(self, request, obj=None):
        # When return True, the link in the left menu is disabled, so we only
        # want to disable changing permissions when we are in the payments view
        # like the list or the detail, but from other views we want to be able
        # to click in the Payment menu button.
        # TODO: understand why change permission applies also to the menu link
        if '/payment/' in request.path:
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        return False
