from django.apps import AppConfig


class ScrapersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "scrapers"

    def ready(self):
        import scrapers.signals  # noqa
