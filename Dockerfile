FROM python:3.7 AS builder

WORKDIR /usr/src/app

# set work directory
# WORKDIR /usr/src/app

RUN apt-get update
RUN apt-get install -y libgl1-mesa-dev


# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# RUN pip install watchdog
# RUN pip install pyyaml

# copy project
COPY . .


# RUN apt-get update
# # RUN apt-get install -y ffmpeg libsm6 libxext6 libxrender-dev libomp-dev libgl1-mesa-glx
# RUN apt-get install -y libgl1-mesa-dev

# RUN python3 -m venv /venv
# ENV PATH="/venv/bin:$PATH"

# RUN pip install --upgrade pip

# COPY . .
# RUN pip install --no-cache-dir .
# # why req doesn't
# RUN pip install boto3
# RUN pip install celery==4.4.7
# RUN pip install redis==3.5.3
# RUN pip install opencv-python~=4.5.4.58

# RUN pip install moviepy~=1.0.3
# # RUN pip install moviepy
# RUN pip install deepface==0.0.68
# RUN pip install SpeechRecognition==3.8.1



# FROM python:3.7 AS test_runner
# WORKDIR /tmp
# COPY --from=builder /venv /venv
# COPY --from=builder /usr/src/app/tests tests
# ENV PATH=/venv/bin:$PATH

# # install test dependencies
# # RUN pip install pytest

# # run tests
# # RUN pytest tests


# FROM python:3.7 AS service
# RUN apt-get install -y libgl1-mesa-dev
# WORKDIR /root/app/site-packages
# COPY --from=test_runner /venv /venv
# ENV PATH=/venv/bin:$PATH
