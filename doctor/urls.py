from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import doctor_list, doctor_detail, video_call_with_doctor, chat_with_ai,educational_content

urlpatterns = [
    path('consult', doctor_list, name='doctor_list'),
    path('doctor/<int:doctor_id>/', doctor_detail, name='doctor_detail'),  
    path('video_call/<int:doctor_id>/', video_call_with_doctor, name='video_call_with_doctor'),
    path('chat_with_ai', chat_with_ai, name='chat_with_ai'),
    path('education', educational_content, name='educational_content'),

    ]
