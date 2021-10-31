import speech_recognition as speech_recog
import json
from pydub import AudioSegment
import os


CELEBRITY_DICTIONARY_PATH = os.environ.get(
    'CELEBRITY_DICTIONARY_PATH', "src/celebrities_names.txt")
SR_SLIDINGWINDOW_SEC = os.environ.get('SR_SLIDINGWINDOW_SEC', 3)
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


def search_celebrities2(content, celebrity_list):
    found_text = content.strip().lower()
    for celeb in celebrity_list:
        if celeb in found_text:
            return True


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

    new_sound = AudioSegment.empty()
    last_time_end = 0

    print(f'New sound len: {len(new_sound)}')

    for timestamps in intervals['result']:
        time_start = timestamps['time_start']
        time_end = timestamps['time_end']

        print(f'Mute audio: {time_start} - {time_end}')

        before = sound[last_time_end * 1000 : time_start * 1000]

        #after = sound[time_end * 1000:]
        print(f'New sound len: {len(new_sound)}')
        print(f'Before len: {len(before)}')
        if len(new_sound) == 0:
            new_sound = before
        else:
            new_sound = new_sound.append(before)

        print(f'New sound len (before applied): {len(new_sound)}')

        duration_ms = (time_end - time_start) * 1000
        silence = AudioSegment.silent(duration = duration_ms)

        new_sound = new_sound.append(silence)
        print(f'Silence len: {len(silence)}')
        print(f'New sound len (Silence applied): {len(new_sound)}')
        #new_sound = new_sound.append(after)
        last_time_end = time_end

        #sound = sound.overlay(silence, position=time_start * 1000)
        #sound = sound.fade(to_gain=0, start=time_start * 1000, duration = duration_ms)
        #new_sound = sound.fade(to_gain=-100,
        #                       start=time_start * 1000,
        #                       duration=(time_end - time_start + 1) * 1000)

    rest = sound[last_time_end * 1000:]
    print(f'Rest len: {len(rest)}')

    new_sound = new_sound.append(rest)
    print(f'New sound len (total): {len(new_sound)}')

    new_sound.export(save_path, format='wav', bitrate="192k")

    # sound.export(save_path, format='wav', bitrate="192k")

