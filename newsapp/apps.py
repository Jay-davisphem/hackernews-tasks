from django.apps import AppConfig


class NewsappConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "newsapp"

    def ready(self):
        import newsapp.receivers
        from newsapp import tasks

        tasks.start()
