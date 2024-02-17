from django.shortcuts import render, get_object_or_404
from .models import DoctorProfile, PatientEducation
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import google.generativeai as genai
import pyttsx3
from gtts import gTTS
import os
from googletrans import Translator
import vlc
import speech_recognition as sr


def login(request):
    return render(request, 'pages/sign-in.html')


@login_required
def doctor_list(request):
    # display doctors according to the time only 
    
    doctors = DoctorProfile.objects.all()
    return render(request, 'doctor/doctor_list.html', {'doctors': doctors})

def doctor_detail(request, doctor_id):
    doctor = get_object_or_404(DoctorProfile, pk=doctor_id)
    # Return doctor details as JSON response
    return JsonResponse({
        'doctor_name': doctor.doctor_name,
        'doctor_phone_number': doctor.doctor_phone_number,
        'doctor_timings': doctor.doctor_timings,
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
        speak(response)

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

def speak(text):
    tts = gTTS(text, lang="hi")  # Create a gTTS object
    tts.save("output.mp3")  # Save the synthesized speech as an MP3 file
    # playsound('output.mp3')

    p = vlc.MediaPlayer("output.mp3")
    p.play()
    # Wait for the playback to finish
    while p.get_state() != vlc.State.Ended:
        pass

    # Stop the playback
    p.stop()

    os.remove("output.mp3")

# def get_audio(request):
#     # Your existing get_audio function code
#     r = sr.Recognizer()
#     with sr.Microphone() as source:
#         audio = r.listen(source)
    
#     said = ""
    
#     try:
#         said = r.recognize_google(audio)
#         print(said)
#     except Exception as e:
#         print("Exception: " + str(e))
    
#     return JsonResponse({'audio_text': said})
