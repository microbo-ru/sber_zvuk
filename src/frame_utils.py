from moviepy.editor import *
from PIL import Image
import os
import cv2


def save_frame(frame, path):
    image = Image.fromarray(frame)
    image.save(path)


def get_frames(video_path, frames_save_path):
    # TODO: create meta-file .json
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


def combine_frames(frames_path, save_path, video_file_name, fps=25):
    files = [f for f in os.listdir(frames_path) if os.path.isfile(os.path.join(frames_path, f))]
    # sort by frame pos
    files.sort(key=lambda x: int(x.split("_")[-2]))
    clips = [ImageClip(os.path.join(frames_path,m)).set_duration(1/fps)
             for m in files]

    concat_clip = concatenate_videoclips(clips, method="compose")
    concat_clip.write_videofile(os.path.join(save_path, "test.mp4"), fps=fps)


#get_frames("D:/Загрузки/SampleVideo.mp4", "D:/datasets/sber_zvuk_samples")
#combine_frames("D:/datasets/sber_zvuk_samples", "D:/datasets/")
