#!/bin/bash
xhost +local:docker

# Define the version of the Docker image to use
IMAGE_VERSION="1.1.1"

docker run -d -it \
  --name kortex_humble \
  --gpus all \
  -e NVIDIA_DRIVER_CAPABILITIES=all \
  -e DISPLAY=$DISPLAY \
  -e QT_X11_NO_MITSHM=1 \
  --mount type=bind,source=/tmp/.X11-unix,target=/tmp/.X11-unix \
  --device /dev/dri:/dev/dri \
  --cap-add=sys_nice \
  --ulimit rtprio=99 \
  --ulimit memlock=-1 \
  --net host \
  kortex_humble:${IMAGE_VERSION}
