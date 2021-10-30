from moviepy.editor import *
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

path = "D:/Загрузки/SampleVideo.mp4"

# split(path)
#combine("extracted_video.mp4", "extracted_audio.mp3")
