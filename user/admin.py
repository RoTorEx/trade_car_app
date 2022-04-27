from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from user.models import UserProfile
from user.forms import UserProfileCreationForm, UserProfileChangeForm


class UserProfileAdmin(UserAdmin):
    add_form = UserProfileCreationForm
    form = UserProfileChangeForm
    model = UserProfile
    list_display = ['username', 'email', 'verifyed_email', 'role']

    fieldsets = (
        (_('User info'), {'fields': ('username', 'email', 'verifyed_email', 'password', 'role')}),
    )

    # add_fieldsets = (
    #     (None, {
    #         'classes': ('wide',),
    #         'fields': ('username', 'email', 'password', 'role')}),
    # )


admin.site.register(UserProfile, UserProfileAdmin)
