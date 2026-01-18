from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


# Create your models here.
class User(AbstractUser):
    name = models.CharField(max_length=30)
    date_of_birth = models.DateField(null=True, blank=True)
    mobile = models.CharField(max_length=15)
    role = models.CharField(max_length=30, default="patient")
    image = models.ImageField(upload_to='patients/', null=True, blank=True)

    def __str__(self):
        return self.username
    

#doctor model #####
class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=30, null=True)
    image = models.ImageField(upload_to='doctors/', null=True, blank=True)
    email = models.EmailField()
    specialization = models.CharField(max_length=100, default="doctor")
    experience = models.CharField(max_length=30, default="Experienced consultant")
    fees = models.DecimalField(max_digits=5, decimal_places=2)
    qualification = models.CharField(max_length=200, default="MD")
    time = models.CharField(max_length=100, default="10am to 1pm")

    def __str__(self):
        return self.name




###################appointment model ##########
class Appointment(models.Model):
    patient = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE
    )
    date = models.DateField()
    time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=30, default="pending")

    def __str__(self):
        return f"{self.patient} - {self.doctor} ({self.date})"
    


    



         

