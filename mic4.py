import os
import time
import urllib.parse
import webbrowser
import subprocess
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import whisper
from openai import OpenAI

client = OpenAI()
# Enter your Assistant ID here.
ASSISTANT_ID = ""
# Load the Whisper model
model = whisper.load_model("base")

# Define the wake word
WAKE_WORD = "hello"

# Paths to applications (adjust according to your system)
exe_path_discord = 'C:/Path/To/Discord.exe'
exe_path_slicer = 'C:/Path/To/Slicer.exe'

# Function to convert text to speech and play it
def speak(text):
    tts = gTTS(text=text, lang='en', slow=False)
    temp_file = "temp_speech.mp3"
    tts.save(temp_file)
    playsound(temp_file)
    os.remove(temp_file)

# Function to save and transcribe audio using Whisper
def transcribe_audio_with_whisper(audio_data):
    # Save the captured audio to a file
    audio_file_path = "temp_audio.wav"
    with open(audio_file_path, "wb") as audio_file:
        audio_file.write(audio_data.get_wav_data())
    options = {
        "language": "en"
    }
    result = model.transcribe(audio_file_path, **options)
    # Transcribe the audio file
    #result = model.transcribe(audio_file_path)
    os.remove(audio_file_path)  # Clean up the temporary audio file
    return result["text"]

# Listen for wake word
def listen_for_wake_word():
    with sr.Microphone() as source:
        print("Listening for the wake word...")
        audio = r.listen(source, timeout=10.0)  # Adjust timeout as needed
    return transcribe_audio_with_whisper(audio)

# Main interaction after wake word detection
def main_interaction():
    with sr.Microphone() as source:
        print("I'm listening, what's your command?")
        audio = r.listen(source)
    command = transcribe_audio_with_whisper(audio).lower()
    return command

# Initialize the recognizer
r = sr.Recognizer()

# Main loop
while True:
    try:
        transcription = listen_for_wake_word()
        if WAKE_WORD in transcription.lower():
            print("Wake word detected.")
            command = main_interaction()
            print(f"You said: {command}")

            if "quit" in command:
                print("Exiting...")
                break
            elif "google" in command:
                print("What would you like to search for?")
                query = main_interaction()
                print(f"Searching for: {query}")
                encoded_query = urllib.parse.quote_plus(query)
                webbrowser.open(f"https://www.google.com/search?q={encoded_query}")
                speak("Opening Google")
            elif "discord" in command:
                subprocess.run([exe_path_discord])
                speak("Opening Discord")
            elif "slicer" in command:
                subprocess.run([exe_path_slicer], shell=True)  # Use shell=True if necessary
                speak("Opening Slicer for 3D Printing")
            # Add more commands as needed
            else:
        # Create a thread with a message.
                thread = client.beta.threads.create(
                messages=[
                {
                    "role": "user",
                # Update this with the query you want to use.
                "content": command,
                }
            ]
            )

            # Submit the thread to the assistant (as a new run).
            run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=ASSISTANT_ID)
            print(f"👉 Run Created: {run.id}")

        # Wait for run to complete.
            while run.status != "completed":
                run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
                print(f"🏃 Run Status: {run.status}")
                time.sleep(1)
            else:
                print(f"🏁 Run Completed!")

            # Get the latest message from the thread.
                message_response = client.beta.threads.messages.list(thread_id=thread.id)
                messages = message_response.data

            # Print the latest message.
                latest_message = messages[0]
                print(f"💬 Response: {latest_message.content[0].text.value}")

                text=latest_message.content[0].text.value
        else:
            print("Wake word not detected, listening again...")
            time.sleep(1)  # Short pause before retrying, adjust as needed
    except Exception as e:
        print(f"An error occurred: {e}")
        time.sleep(1)  # Wait a bit before retrying

speak(text)