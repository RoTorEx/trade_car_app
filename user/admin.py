from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from user.models import UserProfile
# from user.forms import UserProfileCreationForm, UserProfileChangeForm

# # Register Users
admin.site.register(UserProfile)


# from django.contrib.auth import get_user_model
# from django.contrib.auth.admin import UserAdmin


# class UserProfileAdmin(UserAdmin):
#     add_form = UserProfileCreationForm
#     form = UserProfileChangeForm
#     model = UserProfile
#     list_display = ['email', 'username', ]


# admin.site.register(UserProfile, UserProfileAdmin)
