import speech_recognition as speech_recog
import json
from pydub import AudioSegment
import os


def get_celebrities_list(path_to_list):
    content = open(path_to_list, encoding='utf-8').readlines()
    celeb_names = []
    for line in content:
        celeb_names.append(line.strip().lower())
    return celeb_names


def get_transcript(audio_file_path, audio_duration, prefix='test'):
    sample_audio = speech_recog.AudioFile(audio_file_path)
    recognizer = speech_recog.Recognizer()
    transcript_list = list()
    celeb_list = get_celebrities_list("src/celebrities_names.txt")
    dur = 2
    for i in range(int(audio_duration) - 1):
        with sample_audio as audio_file:
            audio_content = recognizer.record(audio_file, offset=i, duration=dur)
            try:
                result = recognizer.recognize_google(audio_content, language='ru-RU')
                if search_celebrities(result, celeb_list):
                    print(f"{result}_{float(i)}_{float(i + dur)}")
                    transcript_list.append({"time_start": i,
                                            "time_end": i + dur})
            except speech_recog.UnknownValueError:
                continue
    transcript_list = join_time_interval(transcript_list)
    with open(f"{prefix}_audio.json", 'w') as f:
        json.dump({"result": transcript_list}, f)
    return transcript_list


def join_time_interval(transcript_list):
    last_start = 0
    last_end = -1
    new_transcript = list()
    for row in transcript_list:
        if last_end >= row['time_start']:
            last_end = row['time_end']
        else:
            if last_end != -1:
                new_transcript.append({"time_start": last_start,
                                       "time_end": last_end})
            last_end = row['time_end']
            last_start = row['time_start']
    new_transcript.append({"time_start": last_start,
                           "time_end": last_end})
    return new_transcript


def search_celebrities(content, celebrity_list):
    for celeb in celebrity_list:
        if celeb in content:
            return True


def mute_audio_interval(transcript_json_path, original_audio_path, audio_save_dir, prefix='test'):
    #don't work
    with open(transcript_json_path) as json_data:
        intervals = json.load(json_data)

    save_path = os.path.join(audio_save_dir, f"{prefix}_final_audio.wav")
    sound = AudioSegment.from_file(original_audio_path)

    for timestamps in intervals['result']:
        time_start = timestamps['time_start']
        time_end = timestamps['time_end']
        print(time_start, time_end)
        new_sound = sound.fade(to_gain=-100, start=time_start * 1000, duration=(time_end-time_start+1) * 1000 )
        new_sound.export(save_path, format='wav', bitrate="192k")

    #sound.export(save_path, format='wav', bitrate="192k")


# get_transcript("D:/datasets/extracted_audio.wav", 198)

mute_audio_interval('test_audio.json', 'D:/datasets/extracted_audio.wav', 'D:/datasets/')
