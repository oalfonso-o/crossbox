from django.contrib import admin


class SubscriberAdmin(admin.ModelAdmin):
    list_display = 'username', 'first_name', 'last_name', 'wods'
    search_fields = [
        'user__first_name', 'user__last_name', 'user__username', 'wods'
    ]
    ordering = ['user', 'wods']
