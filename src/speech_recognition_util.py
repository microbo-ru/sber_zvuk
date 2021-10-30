import speech_recognition as speech_recog


def get_transcript(audio_file_path, audio_duration):
    sample_audio = speech_recog.AudioFile(audio_file_path)
    recognizer = speech_recog.Recognizer()
    for i in range(int(audio_duration) - 1):
        with sample_audio as audio_file:
            audio_content = recognizer.record(audio_file, offset=i, duration=2)
            try:
                result = recognizer.recognize_google(audio_content, language='ru-RU')
                print(f"{i}: ", result)
            except speech_recog.UnknownValueError:
                continue


#get_transcript("D:/datasets/extracted_audio.wav", 198)
