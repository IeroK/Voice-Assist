import speech_recognition as sr
import subprocess
import whisper

model = whisper.load_model("base")
def detect_wake_word():
    # Initialize recognizer
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    # Monitor microphone for the wake word
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening for wake word...")
        audio = recognizer.listen(source)

        # Change "wake_word" to your actual wake word
        try:
            text = recognizer.recognize_google(audio)
            if "hello" in text.lower():
                return True
        except sr.UnknownValueError:
            print("Could not understand audio")
        return

def record_audio():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    # Record audio upon wake word detection
    with mic as source:
        print("Recording...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

        # Save the audio file
        with open("temp_audio.wav", "wb") as f:
            f.write(audio.get_wav_data())
    return "temp_audio.wav"

def transcribe_audio(audio_path):
    # Transcribe audio using Whisper
    #result = subprocess.run(["whisper", audio_path,], capture_output=True, text=True)
    result = model.transcribe(audio_path)
    return result.stdout
def main():
    if detect_wake_word():
        audio_path = record_audio()
        print("Transcribing...")
        transcription = transcribe_audio(audio_path)
        print("Transcription:", transcription)

if __name__ == "__main__":
    main()