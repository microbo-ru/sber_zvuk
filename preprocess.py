from moviepy.editor import *
from PIL import Image
import os


def split(video_path, save_path):
    original_video = VideoFileClip(video_path)

    audio_clip = original_video.audio
    audio_clip.write_audiofile(os.path.join(save_path, "extracted_audio.mp3"))
    audio_clip.close()

    muted_video = original_video.without_audio()
    muted_video.write_videofile(os.path.join(save_path, "extracted_video.mp4"))

    original_video.close()
    muted_video.close()


def combine(video_path, audio_path):
    video_clip = VideoFileClip(video_path)
    audio_clip = AudioFileClip(audio_path)

    video_clip = video_clip.set_audio(audio_clip)
    video_clip.write_videofile("combined_video.mp4")

    audio_clip.close()
    video_clip.close()


def save_frame(frame, path):
    image = Image.fromarray(frame)
    image.save(path)


def get_frames(video_path, frames_save_path):
    video_clip = VideoFileClip(video_path)

    frame_prefix_name = video_path.split('/')[-1].split('.')[-2]
    if not os.path.isdir(frames_save_path):
        os.mkdir(frames_save_path)
    num_of_frames = int(video_clip.fps * video_clip.duration)

    counter = 0
    for frame in video_clip.iter_frames():
        # format the file name and save it
        frame_duration_formatted = (counter / num_of_frames) * video_clip.duration * 100
        frame_filename = os.path.join(frames_save_path,
                                      f"{frame_prefix_name}_{counter}_{frame_duration_formatted}.jpg")
        # save the frame with the current duration
        save_frame(frame, frame_filename)
        counter += 1
    print(f"{counter} frames saved")
    video_clip.close()


path = "D:/Загрузки/SampleVideo.mp4"

# split(path)
# combine("extracted_video.mp4", "extracted_audio.mp3")

get_frames(path, "img_data_new")
