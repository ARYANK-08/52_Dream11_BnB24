from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import login,doctor_list, doctor_detail, video_call_with_doctor, chat_with_ai,educational_content,patient_profile,check_patient_profile
from .views import patient_list, fill_report, index

urlpatterns = [
    path('', index,name='index'),
    path('login', login, name='login'),
    path('doctor_list', doctor_list, name='doctor_list'),
    path('doctor/<int:doctor_id>/', doctor_detail, name='doctor_detail'),  
    path('video_call/<int:doctor_id>/', video_call_with_doctor, name='video_call_with_doctor'),
    path('chat_with_ai', chat_with_ai, name='chat_with_ai'),
    path('education', educational_content, name='educational_content'),
    path('patient_profile', patient_profile, name='patient_profile'),
    path('check_patient_profile', check_patient_profile,name='check_patient_profile'),
    path('patient_list/', patient_list, name='patient_list'),
    path('fill_report/<int:patient_id>/', fill_report, name='fill_report'),
    
]
