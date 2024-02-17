from django.contrib import admin
from .models import DoctorProfile, PatientEducation
# Register your models here.
admin.site.register(DoctorProfile)
admin.site.register(PatientEducation)