from django.shortcuts import render,HttpResponse, redirect

# Create your views here.

from keras.layers import Dense
from keras.models import Sequential, load_model
# from pushbullet import PushBullet
import joblib
import numpy as np
from keras.applications.vgg16 import preprocess_input
import pickle
import cv2
from django.conf import settings
from werkzeug.utils import secure_filename
import os 
from django.contrib import messages
from django.core.files.storage import FileSystemStorage




# Loading Models
covid_model = load_model('models/covid.h5')
braintumor_model = load_model('models/braintumor.h5')
alzheimer_model = load_model('models/alzheimer_model.h5')
diabetes_model = pickle.load(open('models/diabetes.sav', 'rb'))
heart_model = pickle.load(open('models/heart_disease.pickle.dat', "rb"))
pneumonia_model = load_model('models/pneumonia_model.h5')
breastcancer_model = joblib.load('models/cancer_model.pkl')

def diseases(request):
    return render(request, 'disease/homepage.html')

def covid(request):
    return render(request, 'disease/covid.html')

def braintumour(request):
    return render(request, 'disease/braintumor.html')

def breastcancer(request):
    return render(request, 'disease/breastcancer.html')

def diabetes(request):
    return render(request, 'disease/diabetes.html')

def heartdisease(request):
    return render(request, 'disease/heartdisease.html')

def pneumonia(request):
    return render(request, 'disease/pneumonia.html')

def alzheimer(request):
    return render(request, 'disease/alzheimer.html')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in settings.ALLOWED_EXTENSIONS

def resultc(request):
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        file = request.FILES['file']

        if file and allowed_file(file.name):
            # filename = secure_filename(file.filename)
            fs = FileSystemStorage(location=settings.MEDIA_ROOT)
            filename = fs.save(file.name, file)
            messages.success(request,'Image successfully uploaded and displayed below')
            img = cv2.imread('media/'+filename)
            img = cv2.resize(img, (224, 224))
            img = img.reshape(1, 224, 224, 3)
            img = img/255.0
            pred = covid_model.predict(img)
            if pred < 0.5:
                pred = 0
            else:
                pred = 1

            context = {
                'filename': filename,
                'fn': firstname,
                'ln': lastname,
                'age': age,
                'r': pred,
                'gender': gender,
            }
            # pb.push_sms(pb.devices[0],str(phone), 'Hello {},\nYour COVID-19 test results are ready.\nRESULT: {}'.format(firstname,['POSITIVE','NEGATIVE'][pred]))
            return render(request,'disease/resultc.html', context)

        else:
            messages.error(request,'Allowed image types are - png, jpg, jpeg')
            return redirect(request.url)