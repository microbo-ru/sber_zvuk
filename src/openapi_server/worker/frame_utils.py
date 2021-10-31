from moviepy.editor import *
from PIL import Image
import os
import json

from celery.utils.log import get_task_logger

import deepface
from mtcnn.mtcnn import MTCNN
from pathlib import Path

from deepface import DeepFace
import cv2

logger = get_task_logger(__name__)

def save_frame(frame, path):
    image = Image.fromarray(frame)
    image.save(path)


def get_frames(video_path, frames_save_path):
    # TODO: create meta-file .json
    video_clip = VideoFileClip(video_path)

    video_fps = video_clip.fps
    video_name = video_path.split('/')[-1]
    video_duration = video_clip.duration

    logger.info(f'{video_path} {video_fps} {video_name} {video_duration}')

    frame_prefix_name = video_path.split('/')[-1].split('.')[-2]
    if not os.path.isdir(frames_save_path):
        os.mkdir(frames_save_path)
    num_of_frames = int(video_fps * video_duration)

    counter = 0
    for frame in video_clip.iter_frames():
        if counter > 100:
            break
        # format the file name and save it
        
        # frame_duration_formatted = (counter / num_of_frames) * video_clip.duration * 100
        # frame_filename = os.path.join(frames_save_path,
        #                               f"{frame_prefix_name}_{counter}_{frame_duration_formatted}.jpg")
        frame_filename = os.path.join(frames_save_path, f"{counter}.jpg")
        # save the frame with the current duration
        save_frame(frame, frame_filename)
        counter += 1

    print(f"{counter} frames saved")
    video_clip.close()

    
    
    # build JSON-file
    data = {"name": video_name,
            "duration": video_duration,
            "fps": video_fps,
            "number_of_frames": counter}
    logger.info(data)

    with open(os.path.join(frames_save_path, "metadata.json"), "w") as file:
        json.dump(data, file)



def combine_frames(frames_path, save_path, video_file_name, fps=25):
    files = [f for f in os.listdir(frames_path) if os.path.isfile(os.path.join(frames_path, f))]
    # sort by frame pos
    files.sort(key=lambda x: int(x.split("_")[-2]))

    clips = [ImageClip(os.path.join(frames_path, m)).set_duration(1 / fps)

             for m in files]

    concat_clip = concatenate_videoclips(clips, method="compose")
    concat_clip.write_videofile(os.path.join(save_path, f"{video_file_name}.mp4"), fps=fps)

detector = MTCNN()


def detect_celebs(folder):
    for i in os.listdir(folder):
        logger.info("FFFFFFFF")
        try:
            # faces = DeepFace.detectFace(f'{i}')
            faces = detector.detect_faces(fp)
            logger("detected: " , len(faces))
            for f in faces:
                box = f['box']
                corner_1 = box[0], box[1] + box[3]
                corner_2 = box[0] + box[2], box[1]
                logger.info('box' + box)
                image = cv2.imread(str(fp))
                roi = image[box[1]:box[1] + box[3], box[0]:box[0] + box[2]]
                roi = (0, 0, 255)
                cv2.imwrite(image, str(fp))
                logger.info(f"Write new image {i}")
        except Exception as e:
            logger.info(e)


