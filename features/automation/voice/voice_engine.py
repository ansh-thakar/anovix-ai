import speech_recognition as sr

class VoiceEngine:
    def __init__(self, language="en-IN"):
        self.recognizer = sr.Recognizer()
        self.language = language
        self.microphone = sr.Microphone()
        self.listening = False

    def listen_once(self, timeout=5, phrase_time_limit=6):
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = self.recognizer.listen(
                source,
                timeout=timeout,
                phrase_time_limit=phrase_time_limit
            )
        return self.recognizer.recognize_google(audio, language=self.language)
