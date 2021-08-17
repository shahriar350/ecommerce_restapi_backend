from django.apps import AppConfig


class NonUserAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'non_user_app'
