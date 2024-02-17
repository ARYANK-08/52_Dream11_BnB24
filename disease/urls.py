from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import diseases, covid, resultc, braintumour,breastcancer,alzheimer,diabetes,pneumonia,heartdisease

urlpatterns = [
    path('', diseases, name='diseases'),

    path('covid/', covid, name='covid'),
    path('braintumour/', braintumour, name='braintumour'),
    path('breastcancer/', breastcancer, name='breastcancer'),
    path('alzheimer/', alzheimer, name='alzheimer'),
    path('diabetes/', diabetes, name='diabetes'),
    path('pneumonia/', pneumonia, name='pneumonia'),
    path('heartdisease/', heartdisease, name='heartdisease'),
    

    path('resultc/', resultc, name='resultc'),

    ]