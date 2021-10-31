from moviepy.editor import *
import os
import cv2
import deepface


from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

def split_video(video_path, prefix, out_dir):
    logger.info(f'{video_path} {prefix} {out_dir}')
    original_video = VideoFileClip(video_path)

    audio_clip = original_video.audio
    audio_clip.write_audiofile(os.path.join(out_dir, f'{prefix}_extracted_audio.wav'), codec='pcm_s16le')
    audio_clip.close()

    muted_video = original_video.without_audio()
    muted_video.write_videofile(os.path.join(out_dir, f'{prefix}_extracted_video.mp4'))

    original_video.close()
    muted_video.close()
    logger.info("Success")


def combine_video(video_path, audio_path, res_combined):
    video_clip = VideoFileClip(video_path)
    audio_clip = AudioFileClip(audio_path)

    video_clip = video_clip.set_audio(audio_clip)
    video_clip.write_videofile(res_combined)

    audio_clip.close()
    video_clip.close()
