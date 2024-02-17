from django.contrib import admin
from .models import DoctorProfile, PatientEducation, PatientProfile, PatientReport
# Register your models here.
admin.site.register(DoctorProfile)
admin.site.register(PatientEducation)
admin.site.register(PatientProfile)
admin.site.register(PatientReport)