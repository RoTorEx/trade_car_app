from django.apps import AppConfig


class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user'
    verbouse_name = 'users'
    # label = 'Users'

    # def ready(self):
    #     import user.signals
