#!/bin/bash
xhost +local:docker

docker run -d -it \
  --name kortex \
  --gpus all \
  -e NVIDIA_DRIVER_CAPABILITIES=all \
  -e DISPLAY=$DISPLAY \
  -e QT_X11_NO_MITSHM=1 \
  --mount type=bind,source=/tmp/.X11-unix,target=/tmp/.X11-unix \
  --device /dev/dri:/dev/dri \
  kortex_jazzy:1.2.2