# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.contrib.auth import get_user_model
# from django.utils.timezone import now  # Import timezone-aware datetime
# from employees.models import Employee

# User = get_user_model()

# @receiver(post_save, sender=User)
# def create_employee_profile(sender, instance, created, **kwargs):
#     """Automatically creates an Employee profile when a new User is created."""
#     if created:
#         Employee.objects.create(
#             user=instance,
#             position="New Employee",
#             phone="000000000",
#             hire_date=now()  # Automatically set the hire_date
#         )
