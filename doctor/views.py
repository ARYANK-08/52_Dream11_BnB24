from django.shortcuts import render, get_object_or_404
from .models import DoctorProfile, PatientEducation
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import google.generativeai as genai
import pyttsx3

from django.shortcuts import render, redirect
from .models import PatientProfile
from .forms import PatientProfileForm

from social_django.models import UserSocialAuth

from django.shortcuts import redirect
from django.shortcuts import render, redirect
from .models import PatientReport
from .forms import PatientReportForm

from django.shortcuts import render, redirect
from .models import UserSocialAuth, PatientReport
from .forms import PatientReportForm
from django.conf import settings
from twilio.rest import Client

def index(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'pages/sign-in.html')

from django.shortcuts import render
from .models import DoctorProfile
from datetime import datetime, time
import pytz

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import DoctorProfile
from datetime import datetime, time
import pytz

def doctor_list(request):
    # Get current Indian time
    current_time = datetime.now(pytz.timezone('Asia/Kolkata')).time()

    # Filter doctors based on current time falling within their availability timings
    available_doctors = []
    for doctor in DoctorProfile.objects.all():
        if doctor.doctor_start_time and doctor.doctor_end_time:  # Check if the fields are not None
            if doctor.doctor_start_time <= current_time <= doctor.doctor_end_time:
                available_doctors.append(doctor)

    print(f"hi{available_doctors}")

    return render(request, 'doctor/doctor_list.html', {'doctors': available_doctors})

def doctor_detail(request, doctor_id):
    doctor = get_object_or_404(DoctorProfile, pk=doctor_id)
    # Return doctor details as JSON response
    return JsonResponse({
        'doctor_name': doctor.doctor_name,
        'doctor_phone_number': doctor.doctor_phone_number,
        'doctor_timings': f"{doctor.doctor_start_time} - {doctor.doctor_end_time}",
        'doctor_bio': doctor.doctor_bio,
        'doctor_room_id': doctor.doctor_room_id,
    })

def video_call_with_doctor(request, doctor_id):
    doctor = get_object_or_404(DoctorProfile, pk=doctor_id)
    return render(request, 'doctor/video_call_with_doctor.html', {'doctor': doctor})


def educational_content(request):
    # Retrieve all instances of PatientEducation from the database
    educational_topics = PatientEducation.objects.all()

    # Extract video IDs from the URLs and add them to the context
    video_ids = []
    for topic in educational_topics:
        video_url = topic.url
        video_id = None
        
        # Check if the video URL contains 'v='
        if 'v=' in video_url:
            # Split the URL at 'v=' and take the second part
            video_id = video_url.split('v=')[1]
        
        video_ids.append(video_id)
    print(video_ids)
    context = {
        'educational_topics': educational_topics,
        'video_ids': video_ids,  # Pass the list of video IDs to the template
    }

    return render(request, 'patient/education.html', context)
#Chat with AI Doctor

def chat_with_ai(request):
    if request.method == 'POST':
        user_input = request.POST.get('user_input', '')
        response = get_ai_response(user_input)
        
        # Read out the response using pyttsx3
      
        print(response)
        return render(request, 'doctor/ai.html', {'user_input': user_input, 'response': response})
    return render(request, 'doctor/ai.html', {})

def get_ai_response(user_input):
    genai.configure(api_key="AIzaSyA4uR6gq5njTMtQXJwSpIdq_zC1LA1ugS0")  # Set up your API key
    generation_config = {  # Your generation config
        "temperature": 0.9,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 2048,
    }
    safety_settings = [  # Your safety settings
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        # Add other settings as needed
    ]
    model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                  generation_config=generation_config,
                                  safety_settings=safety_settings)
    convo = model.start_chat(history=[])
    context = "you are an hindi ai doctor who suggests patients and consults them about their problems regarding health "
    message = f"{context} {user_input}"
    response = convo.send_message(message)
    answer = convo.last.text
    # print(f'hi{answer}')
    return convo.last.text # Assuming 'message' contains the response text





def check_patient_profile(request):
    try:
        user_social_auth = UserSocialAuth.objects.filter(user=request.user).first()
        if user_social_auth:
            profile = PatientProfile.objects.filter(user=user_social_auth).first()
            if profile:
                return redirect('doctor_list')
        return redirect('patient_profile')
    except AttributeError:
        return redirect('login')  # Redirect to login if user is not authenticated

def patient_profile(request):
    try:
        user_social_auth = UserSocialAuth.objects.filter(user=request.user).first()
        if not user_social_auth:
            return redirect('login')  # Redirect to login if user has no associated social auth

        if request.method == 'POST':
            form = PatientProfileForm(request.POST)
            if form.is_valid():
                profile = form.save(commit=False)
                profile.user = user_social_auth
                profile.save()
                return redirect('doctor_list')
        else:
            form = PatientProfileForm()
        
        return render(request, 'patient/patient_profile_form.html', {'form': form})
    except UserSocialAuth.DoesNotExist:
        return redirect('login')  # Redirect to login if user is not authenticated


def fill_patient_report(request):
    if request.method == 'POST':
        form = PatientReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.user = request.user.social_auth.get(provider='provider_name')  # Assuming 'provider_name' is the name of the provider used for authentication
            report.save()
            return redirect('doctor_dashboard')  # Redirect to doctor dashboard or any other appropriate page
    else:
        form = PatientReportForm()
    
    return render(request, 'patient_report.html', {'form': form})




def patient_list(request):
    # Retrieve the list of users
    patients = UserSocialAuth.objects.all()
    return render(request, 'patient/patient_list.html', {'patients': patients})



def send_report_via_sms(report, patient_name, dr_name):
    # Twilio credentials
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    twilio_number = settings.TWILIO_PHONE_NUMBER

    # Initialize Twilio client
    client = Client(account_sid, auth_token)

    # Compose the message body
    message_body = f"Patient Name: {patient_name}\nDoctor Name: {dr_name}\nDisease: {report.disease}\nPrecaution: {report.precaution}\nMedication: {report.medication}"


    # Send the report via SMS
    message = client.messages.create(
        body=message_body,
        from_=twilio_number,
        to='+918657689680'  # Assuming phone_number is stored in UserSocialAuth model
    )
    message1 = client.messages.create(
        from_='whatsapp:+14155238886',
        body=message_body,
        to='whatsapp:+918657689680'
            )


    # Print the message SID for reference
    print("Message SID:", message.sid)

def fill_report(request, patient_id):
    patient = get_object_or_404(UserSocialAuth, pk=patient_id)
    if request.method == 'POST':
        form = PatientReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.user = patient  # Assign the UserSocialAuth instance directly
            report.save()
            
            # Get patient and doctor names
            patient_name = f"{patient.user.first_name} {patient.user.last_name}"
            dr_name = report.dr_name.doctor_name  # Assuming dr_name is stored in DoctorProfile model

            # Send the report via SMS
            send_report_via_sms(report, patient_name, dr_name)

            return redirect('chat_with_ai')  # Redirect to success page
    else:
        form = PatientReportForm()
    
    return render(request, 'patient/patient_report.html', {'form': form, 'patient': patient})

