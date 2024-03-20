import speech_recognition as sr
import pyaudio
import time
import whisper

model = whisper.load_model("base")
def listen_for_wake_word(recognizer, microphone, wake_word):
    while True:
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            print("Listening for wake word...")
            audio = recognizer.listen(source)
            try:
                speech_as_text = recognizer.recognize_google(audio).lower()
                if wake_word in speech_as_text:
                    print(f"Wake word '{wake_word}' detected.")
                    return True
            except sr.UnknownValueError:
                print("Could not understand audio")
            except sr.RequestError as e:
                print(f"Could not request results; {e}")

def record_after_wake_word(recognizer, microphone, seconds=5):
    print(f"Recording for {seconds} seconds. Start speaking...")
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source, timeout=seconds)
        
    print("Recording stopped. Processing...")
    return audio

def main():
    wake_word = "hello"  # Define your wake word here
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    if listen_for_wake_word(recognizer, microphone, wake_word):
        # Record after wake word detected
        recorded_audio = record_after_wake_word(recognizer, microphone, seconds=10)
        # You can then process `recorded_audio` as needed, e.g., save it or recognize speech from it
        try:
            print("Recognizing speech...")
            text = model.transcribe(recorded_audio)
            print(f"Transcription: {text}")
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand the audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")

if __name__ == "__main__":
    main()