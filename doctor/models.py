from django.db import models


class DoctorProfile(models.Model):
    doctor_name = models.CharField(max_length=100, null=True, blank=True)
    doctor_image = models.ImageField(upload_to='doctor_images/')
    doctor_timings = models.DateTimeField()
    doctor_bio = models.CharField(max_length=255)  # Specify the max_length for CharField
    doctor_room_id = models.CharField(max_length=20,null=True, blank=True) 
    doctor_phone_number = models.CharField(max_length=20,null=True, blank=True)  # Assuming maximum length for phone number
    
    def __str__(self):
        return self.doctor_name


# class GetHealthTruck(models.Model):
#     user_location = models.CharField()

class PatientEducation(models.Model):
    topic = models.CharField(max_length=20)
    url = models.URLField(max_length=100)
    
    def __str__(self):
        return f'{self.topic} - {self.url}'
