from django.contrib import admin

# Register your models here.
from account.models import User


class UserAdmin(admin.ModelAdmin):

    actions = ['mark_paid_dues', 'unmark_paid_dues', 'set_as_active', 'set_as_inactive']

    def mark_paid_dues(self, request, queryset):
        rows_updated = queryset.update(paid_dues=True)
        self.message_user(request, "Successfully marked %s user(s) dues as paid." % rows_updated)
    mark_paid_dues.short_description = "Mark selected users dues as paid"

    def unmark_paid_dues(self, request, queryset):
        rows_updated = queryset.update(paid_dues=False)
        self.message_user(request, "Successfully marked %s user(s) dues as unpaid." % rows_updated)
    unmark_paid_dues.short_description = "Mark selected users dues as unpaid"

    def set_as_active(self, request, queryset):
        rows_updated = queryset.update(is_active=True)
        self.message_user(request, "Successfully marked %s user(s) as active." % rows_updated)
    set_as_active.short_description = "Set selected users as active"

    def set_as_inactive(self, request, queryset):
        rows_updated = queryset.update(is_active=False)
        self.message_user(request, "Successfully marked %s user(s) as inactive." % rows_updated)
    set_as_inactive.short_description = "Set selected users as inactive"

    list_display = ['get_full_name', 'is_active', 'paid_dues', 'grad_year']
    ordering = ['first_name']
    list_filter = ['is_active', 'grad_year', 'paid_dues']
    search_fields = ['first_name']


admin.site.register(User, UserAdmin)