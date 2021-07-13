from django.apps import AppConfig


class UsermartConfig(AppConfig):
    name = 'UserMart'

    def ready(self):
        import UserMart.signals
