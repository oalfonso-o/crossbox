from django.contrib import admin

from crossbox.models.session_template import SessionTemplate


class SessionTemplateAdminInline(admin.TabularInline):
    model = SessionTemplate
    ordering = ['day__weekday']

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class WeekTemplateAdmin(admin.ModelAdmin):
    inlines = (SessionTemplateAdminInline,)
    list_display = ('name', 'default')
    search_fields = ['name', 'default']
    ordering = ['name', 'default']
