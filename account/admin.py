from django import forms
from django.contrib import admin

# Register your models here.
from django.contrib.admin.helpers import ActionForm
from django.core.mail import send_mass_mail

from account.models import User

EMAIL = 'commissioner@ballsincups.cc'


class SendEmailForm(ActionForm):
    subject = forms.CharField(required=False)
    message = forms.CharField(widget=forms.Textarea, required=False)


class UserAdmin(admin.ModelAdmin):

    action_form = SendEmailForm

    actions = ['mark_paid_dues', 'unmark_paid_dues', 'set_as_active', 'set_as_inactive', 'send_users_mail']

    def send_users_mail(self, request, queryset, subject=None, body=None):
        if not subject:
            subject = '[CCLeague] ' + request.POST['subject']
        if not body:
            body = request.POST['message'] + "\n - The Commissioner"
        emails = []
        for user in queryset:
            emails.append(user.email)
        message = (subject, body, EMAIL, emails)
        send_mass_mail((message,))
        self.message_user(request, "Successfully emailed selected users.")
    send_users_mail.short_description = "Send selected users an email"

    def mark_paid_dues(self, request, queryset):
        rows_updated = queryset.update(paid_dues=True)
        self.send_users_mail(request, queryset, "Dues", "Your dues have been confirmed as paid.")
        self.message_user(request, "Successfully marked %s user(s) dues as paid." % rows_updated)
    mark_paid_dues.short_description = "Mark selected users dues as paid"

    def unmark_paid_dues(self, request, queryset):
        rows_updated = queryset.update(paid_dues=False)
        self.message_user(request, "Successfully marked %s user(s) dues as unpaid." % rows_updated)
    unmark_paid_dues.short_description = "Mark selected users dues as unpaid"

    def set_as_active(self, request, queryset):
        rows_updated = queryset.update(is_active=True)
        self.send_users_mail(request, queryset, "Your account has been activated",
                             "Your account has been reviewed and determined to be a valid member of the CCLeague. "
                             "You may now login to the site at http://www.ballsincups.cc")
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
