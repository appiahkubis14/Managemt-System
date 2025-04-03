from django.apps import AppConfig


class EmployeesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "employees"


    def ready(self):
        import employees.signals  # Ensure signals are loaded
