from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Personal Info
    phone = models.CharField(max_length=15)
    age = models.PositiveIntegerField()
    image = models.ImageField(upload_to="profiles/", blank=True)

    # Hospital Info
    national_id = models.CharField(max_length=14, unique=True)

    # Address
    governorate = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    street = models.CharField(max_length=100, blank=True)

    # Emergency Contact
    emergency_name = models.CharField(max_length=100)
    emergency_phone = models.CharField(max_length=15)
    emergency_relation = models.CharField(max_length=30)

    def __str__(self):
        return self.user.username



class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.ForeignKey("Specialization", on_delete=models.CASCADE)

    def __str__(self):
        return f"Dr. {self.user.username}"
class Specialization(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    def __str__(self):
        return self.name
class DoctorAvailability(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="availabilities")
    day = models.CharField(max_length=10, choices=[
        ("Saturday","Saturday"),
        ("Sunday","Sunday"),
        ("Monday","Monday"),
        ("Tuesday","Tuesday"),
        ("Wednesday","Wednesday"),
        ("Thursday","Thursday"),
        ("Friday","Friday")
    ])
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        unique_together = ("doctor", "day", "start_time", "end_time")

    def __str__(self):
        return f"{self.doctor.user.username} - {self.day} {self.start_time}-{self.end_time}"

class Appointment(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    day = models.CharField(max_length=20)
    time = models.TimeField()
