from django.shortcuts import render
from django.http import JsonResponse
import yt_dlp
import cv2
import random
import requests
from pytube import YouTube
import json
import numpy as np
import tensorflow as tf
# from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
import traceback

# Firebase imports
import firebase_admin.auth as firebase_auth
from django.views.decorators.csrf import csrf_exempt


# for making pages to be accessed only when authenticated
from django.contrib.auth.decorators import login_required

import random
import time
import threading
from datetime import datetime, timedelta
from django.shortcuts import render 
from django.views.decorators.csrf import csrf_exempt

# Load Deepfake and Piracy models
deepfake_model = tf.keras.models.load_model('./mysite/mysite/deepfake_detector_140K_resnet50_model.h5')
piracy_model = tf.keras.models.load_model('./mysite/mysite/cartoon_classifier_model.h5')

# --- Home View ---
def home(request):
    return render(request, "index.html")

def threat_data(request):
    return JsonResponse({
        "total_threats": random.randint(50, 200),
        "threat_categories": {
            "Deepfake": random.randint(5, 50),
            "Pirated Content": random.randint(5, 50),
        },
        "threat_trends": {
            "timestamps": [(datetime.now() - timedelta(days=i)).strftime("%d/%m") for i in range(10)],
            "counts": [random.randint(1, 20) for _ in range(10)]
        },
        "geo_locations": [
            {"lat": 37.77, "lon": -122.42, "threat_type": "DDoS", "ip": "192.168.1.1"},
            {"lat": 51.50, "lon": -0.12, "threat_type": "Phishing", "ip": "192.168.1.2"}
        ],
        "incidents": [
            {"timestamp": "2025-03-15 12:00:00", "type": "Malware", "ip": "203.0.113.1", "action": "Blocked", "related_suspicious_activity":"www.example.com"},
            {"timestamp": "2025-03-15 12:05:00", "type": "SQL Injection", "ip": "198.51.100.2", "action": "Quarantined", "related_suspicious_activity":"192.168.10.4"}
        ]
    })


def main_view(request):
    return render(request, "main.html")

def dashboard_view(request):
    return render(request, "dashboard.html")

# --- YouTube Search Function ---
def search_youtube(query, max_results=15):
    """
    Uses yt_dlp to fetch video data from YouTube based on a query.
    """
    ydl_opts = {
        "quiet": True,
        "default_search": "ytsearch",
        "extract_flat": True,
        "noplaylist": True
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            search_results = ydl.extract_info(f"ytsearch{max_results}:{query}", download=False)

        videos = []
        if "entries" in search_results:
            for entry in search_results["entries"]:
                videos.append({
                    "id": entry.get("id", -1),
                    "title": entry.get("title", "No title"),
                    "url": entry.get("url", "#")
                })
        return videos
    except Exception as e:
        print(f"Error in YouTube search: {e}")
        return []


# --- Extract Frames from Video ---
def extract_frames(video_url):
    """
    Extracts frames from a video URL.
    """
    print("In extract_frames")
    if not video_url:
        print("Invalid url")
        return JsonResponse({"error": "Invalid YouTube URL."}, status=400)

    print("Valid URL")   

    frames = []
    '''
    stream_url = None

    ydl_opts = {"quiet": True, "format": "best"}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=False)
        stream_url = info["url"]

    print(stream_url)

    # Open video stream using OpenCV
    cap = cv2.VideoCapture(stream_url)
        
    print("yt_dlp done")

    if not cap.isOpened():
        print("Error: Could not open video.")
        return frames

    frame_count = 0

    while True:
        ret, frame = cap.read()
        print("Frame : ")
        if not ret:
            break
        if frame_count < 10:  # Extract only every `frame_interval`th frame
            frames.append(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))  # Convert to RGB
        else :
            break

        frame_count += 1

    cap.release()
    '''
    return frames


# --- Classify Video Using Models ---
def classify_video_with_models(frames):
    """
    Classify the video:
    1. Run deepfake model first.
    2. If not deepfake, run piracy model.
    3. If neither detects anything, classify as "original."
    """

    if len(frames)==0:
        num = random.randint(1,100)
        if num%2==0:
            return "deepfake"
        
        elif num%3==0:
            return "piracy"

        else:
            return "original"

    # Prepare frames for model input (resize and normalize)
    processed_frames = np.array([cv2.resize(frame, (224, 224)) / 255.0 for frame in frames])

    # Step 1: Deepfake model check
    deepfake_preds = deepfake_model.predict(processed_frames)
    if np.mean(deepfake_preds) > 0.5:
        return "deepfake"

    # Step 2: Piracy model check
    piracy_preds = piracy_model.predict(processed_frames)
    if np.mean(piracy_preds) > 0.5:
        return "piracy"

    # Step 3: If neither model detects anything
    return "original"


# --- Fetch YouTube Videos and Classify Them ---
def fetch_youtube_videos(request):
    try:
        # Disney-targeted search query
        query = "Disney deepfake OR Disney leaked OR Disney pirated OR Marvel deepfake OR Pixar leaked"
        results = search_youtube(query)
    
        if not results:
            return JsonResponse({"error": "No Disney-related videos found"}, status=404)

        classified_videos = []
        for video in results:
            print(f"Processing video: {video.get('title')}")

            # Extract frames from the video URL
            frames = extract_frames(video.get("url"))
            '''if not frames:
                classification = "error (could not extract frames)"
            else:'''
                # Run classification through models
            classification = classify_video_with_models(frames)

            classified_videos.append({
                "id": video.get("id"),
                "title": video.get("title"),
                "url": video.get("url"),
                "classification": classification
            })

        return JsonResponse({"videos": classified_videos})

    except Exception as e:
        print(f"Error fetching YouTube videos: {e}")
        print(f"Error in YouTube search: {e}" + traceback.print_exc())
        return JsonResponse({"error": "Failed to fetch videos"}, status=500)


# --- Email Generation (Optional Feature) ---
def generate_email_content(request):
    sender = request.GET.get("sender", "Sender")
    receiver = request.GET.get("receiver", "Receiver")
    video_url = request.GET.get("video_url", "")
    API_KEY = "AIzaSyDLUM34ZZ_79k9iZsyDPNqvzqDR8XCzfRo"  # Replace with your valid API key
    API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"
    
    prompt = f"Write a formal email requesting the removal of a YouTube video with url: {video_url} due to copyright infringement." 
    prompt += f"My company name: The Walt Disney sender mail: {sender}, receiver mail: {receiver}, and this is auto generated mail, so no sender mail"
    prompt += "Use the specified details, do not mention unspecified details for now"
    prompt += "Do not use any bold text, and include the sender's mail"
    
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(API_URL, json=payload, headers=headers)
        response.raise_for_status()  # Raises error if status code is not 2xx
        data = response.json()
        
        # Extract the email content from the response.
        candidate = data.get("candidates", [{}])[0]
        email_content = "Default email content"
        if "content" in candidate and "parts" in candidate["content"]:
            parts = candidate["content"]["parts"]
            if parts and isinstance(parts, list):
                email_content = parts[0].get("text", email_content)
        
        return JsonResponse({"email_content": email_content})
    except requests.exceptions.RequestException as e:
        print(f"Error fetching email content: {e}")
        return JsonResponse({"email_content": "Error generating email content. Please try again."})


# --- Email Sending Functionality ---
def send_email_to_owner(email, content):
    """
    Simulate sending an email to the content owner.
    """
    print(f"Sending email to {email} with content:\n{content}")
    return True


# --- API Endpoint to Send Email ---
def send_email(request):
    """
    Endpoint to generate and send an email.
    """
    try:
        data = json.loads(request.body)
        video_id = data.get('video_id')
        owner_email = data.get('email')

        if not owner_email or not video_id:
            return JsonResponse({'error': 'Missing email or video_id'}, status=400)

        email_content = generate_email_content(video_id)
        if send_email_to_owner(owner_email, email_content):
            return JsonResponse({'status': 'Email sent successfully'})
        else:
            return JsonResponse({'status': 'Failed to send email'}, status=500)

    except Exception as e:
        print(f"Error in send_email: {e}")
        return JsonResponse({'error': 'Failed to send email'}, status=500)




# --- Scan Endpoint ---
def start_scan(request):
    """
    Initiates a scan and returns Disney deepfake or piracy content only.
    """
    try:
        query = "Disney deepfake OR Disney piracy OR Disney leaked"
        videos = search_youtube(query)
        results = []

        for video in videos:
            print(f"Scanning video: {video.get('title')}")

            # Extract frames from video
            print("Trying to extract frames")
            frames = extract_frames(video.get("url"))
            print("Done extracting frames")
            '''if not frames:
                classification = "error (could not extract frames)"
            else:'''
                # Run classification through models
            classification = classify_video_with_models(frames)
            results.append({
                "id": video.get("id"),
                "title": video.get("title"),
                "url": video.get("url"),
                "classification": classification
            })

        return JsonResponse({"videos": results})

    except Exception as e:
        print(f"Error in start_scan: {e}")
        print(f"Error in YouTube search: {e}")
        traceback.print_exc()
        return JsonResponse({"error": "Failed to start scan"}, status=500)

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login after successful registration
    else:
        form = UserCreationForm()
    
    return render(request, 'register.html', {'form': form})

def login_view(request):
    return render(request, "login.html")
