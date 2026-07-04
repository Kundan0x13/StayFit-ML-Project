# StayFit - AI Gym Coach

StayFitis an AI-powered fitness coaching app that uses your webcam to track workout form, count reps, monitor sets, and provide real-time coaching feedback. The app combines computer vision, pose detection, workout tracking, and AI-generated voice guidance to create an interactive home workout assistant.

## Features

- User login with local workout history
- Real-time webcam-based exercise tracking
- AI pose detection using MediaPipe
- Automatic rep and set counting
- Exercise-specific form metrics
- AI coaching feedback using Groq LLM
- Voice feedback using text-to-speech
- Local workout history stored in SQLite
- Supports multiple exercises:
  - Squats
  - Push-ups
  - Biceps Curls
  - Shoulder Press
  - Lunges

## Tech Stack

- Python
- Streamlit
- Streamlit WebRTC
- MediaPipe
- OpenCV
- SQLite
- Pandas
- Groq API
- gTTS

## Project Structure

```text
StayFit/
├── main.py
├── requirements.txt
├── data/
│   └── stayfit.db
├── detectors/
│   ├── squat.py
│   ├── pushup.py
│   ├── biceps_curl.py
│   ├── shoulder_press.py
│   └── lunges.py
├── services/
│   ├── auth/
│   ├── coaching/
│   ├── config/
│   ├── persistence/
│   ├── state/
│   ├── tracking/
│   ├── ui/
│   └── vision/
├── static/
└── ml_models/
    └── pose_landmarker_full.task
```

## How It Works
  The user logs in with a username.
  The user selects an exercise, target sets, and reps per set.
  The webcam starts through Streamlit WebRTC.
  MediaPipe detects body landmarks in real time.
  Exercise-specific detector classes calculate reps and form metrics.
  Workout progress is updated live in the sidebar.
  Completed sets are saved to the local SQLite database.
  The AI coach gives text and voice feedback during the workout.

  
## Exercise Metrics
1. Squats
    Knee angle
    Back angle
    Depth status
2. Push-ups
    Elbow angle
    Body alignment
    Hip position
3. Biceps Curls
    Elbow angle
    Elbow stability
    Swing detection
4. Shoulder Press
    Elbow angle
    Arm extension
    Back arch status
5. Lunges
    Front knee angle
    Torso angle
    Balance status
   
## Notes
    Make sure camera permission is enabled in your browser.
    Use good lighting for better pose detection.
    Keep your full body visible in the camera frame.
    Voice coaching depends on the Groq API and text-to-speech availability.
    Workout history is stored locally in data/stayfit.db.
    
## Future Improvements
  More exercises
  Personalized workout plans
  Better progress analytics
  Streaks and achievements
  Improved voice coaching
  Form score after each workout
  Mobile-friendly layout
  License
  This project is for educational and personal fitness assistance purposes.
