from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from employees.models import Employee
from django.contrib.auth import get_user_model
from employees.models import Employee

User = get_user_model()  # Dynamically gets 'employees.CustomUser'

class Command(BaseCommand):
    help = "Assigns employee profiles to all users without one."

    def handle(self, *args, **kwargs):
        users_without_profiles = User.objects.filter(employee_profile__isnull=True)

        for user in users_without_profiles:
            Employee.objects.create(user=user, position="Staff", phone="000000000")
            self.stdout.write(self.style.SUCCESS(f"Employee profile created for {user.username}"))

        self.stdout.write(self.style.SUCCESS("All missing employee profiles created."))
