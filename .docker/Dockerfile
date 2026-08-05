FROM osrf/ros:jazzy-desktop-full

ENV DEBIAN_FRONTEND=noninteractive
ENV RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
ENV COLCON_WS=/app/workspace/ros2_kortex_ws

SHELL ["/bin/bash", "-c"]

WORKDIR /app

RUN apt-get update && apt-get install -y \
    ros-jazzy-rmw-cyclonedds-cpp \
    python3-colcon-common-extensions \
    python3-vcstool \
    ros-jazzy-moveit* \
    ros-jazzy-parameter-traits \
    xterm \
    terminator \
    tree \
    && rm -rf /var/lib/apt/lists/*

WORKDIR ${COLCON_WS}

RUN mkdir -p src && \
    git clone https://github.com/Curso-de-Robotica-e-IA/kinova_robot_ros2.git -b jazzy src/ros2_kortex && \
    vcs import src --skip-existing --input src/ros2_kortex/ros2_kortex.jazzy.repos && \
    vcs import src --skip-existing --input src/ros2_kortex/ros2_kortex-not-released.jazzy.repos && \
    vcs import src --skip-existing --input src/ros2_kortex/simulation.jazzy.repos

RUN apt-get update && rosdep update && \
    rosdep install --ignore-src --from-paths src -y -r && \
    rm -rf /var/lib/apt/lists/* && \
    source /opt/ros/jazzy/setup.bash && \
    colcon build --cmake-args -DCMAKE_BUILD_TYPE=Release --parallel-workers 1

RUN echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc && \
    echo "source ${COLCON_WS}/install/setup.bash" >> ~/.bashrc && \
    echo 'alias gen3_simulation="ros2 launch kinova_gen3_lite_moveit_config robot.launch.py robot_ip:=xxx.yyy.zzz.www use_sim_time:=true"' >> ~/.bashrc && \
    echo 'alias gen3_moveit_simulation="ros2 launch kinova_gen3_lite_moveit_config robot.launch.py robot_ip:=xxx.yyy.zzz.www use_sim_time:=true"' >> ~/.bashrc && \
    echo 'alias gen3_robot="ros2 launch kortex_bringup gen3_lite.launch.py robot_ip:=192.168.2.10"' >> ~/.bashrc && \
    echo 'alias gen3_moveit_robot="ros2 launch kinova_gen3_lite_moveit_config robot.launch.py robot_ip:=192.168.2.10 use_sim_time:=false"' >> ~/.bashrc && \
    echo 'alias gen3_servo_simulation="ros2 launch kortex_servo_simulation servo.launch.py"' >> ~/.bashrc

CMD ["bash"]