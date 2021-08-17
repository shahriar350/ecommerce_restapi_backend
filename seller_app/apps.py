from django.apps import AppConfig


class SellerAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'seller_app'

    def ready(self):
        import seller_app.signals