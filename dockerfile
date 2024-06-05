# Use a Python base image with TensorFlow pre-installed
FROM python:3.10.5

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#user
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

#
# Install system dependencies for OpenCV
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

# Install system dependencies for dlib
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    libopenblas-dev \
    libjpeg-dev \
    libpng-dev \
    libtiff-dev \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    libv4l-dev \
    libxvidcore-dev \
    libx264-dev \
    libatlas-base-dev \
    gfortran \
    && rm -rf /var/lib/apt/lists/*

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# into this layer.
RUN python -m pip install --upgrade pip
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

# Copy the rest of the application code
COPY . .


COPY /optimizer_fix/optimizer.py ../usr/local/lib/python3.10/site-packages/keras/optimizers/optimizer_experimental/

# Expose the port used by the Flask app
EXPOSE 8000

# Set the environment variable for the model path (modify the path)
# ENV MODEL_PATH=/app/model_3_epoch.h5
# Change this to your model location

# Start the Flask app using gunicorn (recommended for production)
# CMD [ "gunicorn", "--bind", "0.0.0.0:8000", "app:app" ]
CMD python app.py