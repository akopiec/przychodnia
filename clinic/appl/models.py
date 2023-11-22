

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


ROLE = (
    (1, 'doctor'),
    (2, 'patient'),
    (3, 'admin'),
)


class UserManager(BaseUserManager):
    def create_user(self,username,password=None,city=None,street=None,house_number=None,role=None):
        user=self.model(username=username,city=city,street=street,house_number=house_number,role=role)
        user.set_password(password)
        user.save
        return user

    def create_superuser(self, username, password, city=None, street=None, house_number=None, role=None):
        user=self.create_user(username, password=password, city=city, street=street, house_number=house_number, role=role)
        user.is_superuser=True

        user.save
        return user


class UserClinic(AbstractBaseUser):
    username = models.CharField(max_length=100, unique=True, default='')
    city = models.CharField(max_length=30)
    street = models.CharField(max_length=30)
    house_number = models.PositiveIntegerField(blank=True, unique=False, null=True)
    role = models.PositiveIntegerField(choices=ROLE, default=1)
    objects = UserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['city', 'street', 'house_number', 'role']


DAY = ((1, 'Poniedziałek'), (2, 'Wtorek'))

HOUR = ((1, 10), (2, 11), (3, 12))


class Visit(models.Model):
    doctor = models.ForeignKey(UserClinic, on_delete=models.CASCADE, related_name="doctor")
    patient = models.ForeignKey(UserClinic, on_delete=models.CASCADE, related_name="patient")
    day = models.PositiveIntegerField(choices=DAY, default=1)
    hour_from = models.IntegerField(choices=HOUR, default=1)


class Prescription(models.Model):
    doctor = models.ForeignKey(UserClinic, on_delete=models.CASCADE, related_name="doctor_prescription")
    patient = models.ForeignKey(UserClinic, related_name="patient_prescription", on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    medicines = models.CharField(max_length=200)

