#!/bin/bash

# Ensure the script is run with bash
if [ -z "$BASH_VERSION" ]; then
    exec bash "$0" "$@"
fi

# Prompt the user for the ROS_DOMAIN_ID
read -p "Type the ROS_DOMAIN_ID (a integer, except 102 until 214, and lower than 233): " INPUT_DOMAIN
DOMAIN=${INPUT_DOMAIN}

# Validate that the input is an integer and within the specified range
if ! [[ "$DOMAIN" =~ ^[0-9]+$ ]]; then
    echo "Error: The ROS_DOMAIN_ID must be an integer."
    exit 1
fi

if [ "$DOMAIN" -lt 102 ] || [ "$DOMAIN" -gt 214 ]; then
    echo "Error: The ROS_DOMAIN_ID must be between 102 and 214."
    exit 1
fi

if [ "$DOMAIN" -ge 233 ]; then
    echo "Error: The ROS_DOMAIN_ID must be lower than 233."
    exit 1
fi

read -p "Type the ROS_IMAGE_VERSION (default is 1.4.3): " INPUT_VERSION
IMAGE_VERSION=${INPUT_VERSION:-1.4.3}

xhost +local:docker

echo "Starting container with ROS_DOMAIN_ID=${DOMAIN}..."
docker run -d -it \
  --name kortex_humble \
  --gpus all \
  -e NVIDIA_DRIVER_CAPABILITIES=all \
  -e DISPLAY=$DISPLAY \
  -e QT_X11_NO_MITSHM=1 \
  -e ROS_DOMAIN_ID=${DOMAIN} \
  --mount type=bind,source=/tmp/.X11-unix,target=/tmp/.X11-unix \
  --device /dev/dri:/dev/dri \
  --cap-add=sys_nice \
  --ulimit rtprio=99 \
  --ulimit memlock=-1 \
  --net host \
  --ipc host \
  --shm-size=1g \
  kortex_humble:${IMAGE_VERSION}
