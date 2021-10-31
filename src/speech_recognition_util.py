import speech_recognition as speech_recog
import json
from pydub import AudioSegment
import os

CELEBRITY_DICTIONARY_PATH = os.environ.get(
    'CELEBRITY_DICTIONARY_PATH', "src/celebrities_names.txt")
SR_SLIDINGWINDOW_SEC = os.environ.get('SR_SLIDINGWINDOW_SEC', 2)
SR_SHIFT_SEC = os.environ.get('SR_SHIFT_SEC', 1)


# Michael Jakson = Jakson Michael
def reverse_celeb_name(name):
    # splitting the string on space
    words = name.split()
    # reversing the words using reversed() function
    words = list(reversed(words))
    # joining the words and printing
    result = " ".join(words)
    return result


# Returns a list of Celebrities from the dictionary provided
def get_celebrities_list(path_to_list):
    content = open(path_to_list, encoding='utf-8').readlines()
    celeb_names = []
    for line in content:
        name = line.strip().lower()
        reversed = reverse_celeb_name(name)

        celeb_names.append(name)
        celeb_names.append(reversed)
    return celeb_names


def get_transcript(inputaudio_file_path,
                   audio_duration_sec,
                   audio_json_file_path):
    sample_audio = speech_recog.AudioFile(inputaudio_file_path)
    recognizer = speech_recog.Recognizer()
    transcript_list = list()
    celeb_list = get_celebrities_list(CELEBRITY_DICTIONARY_PATH)
    duration = SR_SLIDINGWINDOW_SEC

    for i in range(int(audio_duration_sec) - SR_SHIFT_SEC):
        with sample_audio as audio_file:
            audio_content = recognizer.record(audio_file,
                                              offset=i,
                                              duration=duration)
            try:
                result = recognizer.recognize_google(audio_content,
                                                     language='ru-RU')
                if search_celebrities(result, celeb_list):
                    print(f"{result}_{float(i)}_{float(i + duration)}")
                    transcript_list.append({"time_start": i,
                                            "time_end": i + duration})
            except speech_recog.UnknownValueError:
                continue

    transcript_list = join_time_intervals(transcript_list)
    with open(audio_json_file_path, 'w') as f:
        json.dump({"result": transcript_list}, f)

    return transcript_list


def join_time_intervals(transcript_list):
    firstRow = transcript_list[0]
    last_start = firstRow['time_start']
    last_end = firstRow['time_end']

    new_transcript = list()
    for row in transcript_list:
        if last_end >= row['time_start']:
            last_end = row['time_end']
        else:
            new_transcript.append({"time_start": last_start,
                                   "time_end": last_end})
            last_start = row['time_start']
            last_end = row['time_end']

    new_transcript.append({"time_start": last_start,
                           "time_end": last_end})
    return new_transcript


def search_celebrities(content, celebrity_list):
    found_text = content.strip().lower()
    for celeb in celebrity_list:
        if celeb in found_text:
            return True


def mute_audio_interval(transcript_json_path,
                        original_audio_path,
                        audio_save_dir, prefix='test'):
    # don't work
    with open(transcript_json_path) as json_data:
        intervals = json.load(json_data)

    save_path = os.path.join(audio_save_dir, f"{prefix}_final_audio.wav")
    sound = AudioSegment.from_file(original_audio_path, format="wav")

    for timestamps in intervals['result']:
        time_start = timestamps['time_start']
        time_end = timestamps['time_end']

        print(f'Mute audio: {time_start} - {time_end}')

        duration_ms = (time_end - time_start) * 1000
        silence = AudioSegment.silent(duration = duration_ms)
        sound = sound.overlay(silence, position=time_start * 1000)



        #new_sound = sound.fade(to_gain=-100,
        #                       start=time_start * 1000,
        #                       duration=(time_end - time_start + 1) * 1000)

    sound.export(save_path, format='wav', bitrate="192k")

    # sound.export(save_path, format='wav', bitrate="192k")


# get_transcript("D:/datasets/extracted_audio.wav", 198)

mute_audio_interval('test_audio.json', 'D:/datasets/extracted_audio.wav', 'D:/datasets/')
