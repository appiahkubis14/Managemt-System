from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from utils import get_object_choices, IDGenerator, genderType

# Custom User Model
from django.contrib.auth.models import AbstractUser, Group, Permission

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('staff', 'Staff'),
        ('driver', 'Driver'),
        ('driver_assistant', 'Driver Assistant'),
        ('warehouse_staff', 'Warehouse Staff'),
        ('inventory_manager', 'Inventory Manager'),
        # Add more roles as needed
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='staff')

    groups = models.ManyToManyField(Group, related_name="customuser_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="customuser_permissions", blank=True)

    def is_admin(self):
        return self.role == 'admin'

    def is_manager(self):
        return self.role == 'manager'

    def is_staff_user(self):
        return self.role == 'staff'

    def is_driver(self):
        return self.role == 'driver'

    def is_driver_assistant(self):
        return self.role == 'driver_assistant'

    def is_warehouse_staff(self):
        return self.role == 'warehouse_staff'

    def is_inventory_manager(self):
        return self.role == 'inventory_manager'

    def __str__(self):
        return self.username


# Employee Model
class Employee(models.Model):
    
    department_choices = (
        ('transport', 'Transport'),
        ('warehouse', 'Warehouse'),
        ('inventory', 'Inventory'),
    )
    # employee_id = models.CharField(max_length=64, editable=False, unique=True, null=True)
    employee_name = models.CharField(max_length=255)
    date_of_birth = models.DateField(blank=True, null=True)
    date_of_join = models.DateField(blank=True, null=True)  
    gender = models.CharField(max_length=128, choices=get_object_choices(genderType))
    ghana_card = models.CharField(max_length=128, unique=True)
    phone = models.CharField(max_length=128, unique=True)
    photo = models.ImageField(upload_to="employee_photos/", blank=True, null=True)  
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="employee_profile")
    department = models.CharField(max_length=100 , choices=department_choices)
    position = models.CharField(max_length=100,blank=True, null=True)
    hire_date = models.DateField()
    salary = models.CharField(max_length=100)
    # submitted_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name="submitted_employees")  
    # submitted_on = models.DateTimeField(auto_now_add=True)

    # def save(self, *args, **kwargs):
    #     if not self.employee_id:
    #         generator = IDGenerator()
    #         self.employee_id = generator.generate_unique_id("EMP")
    #     super(Employee, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.position}"

    class Meta:
        verbose_name_plural = "Employees"
