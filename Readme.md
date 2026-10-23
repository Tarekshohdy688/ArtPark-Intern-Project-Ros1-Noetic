# ArtPark Intern Project ROS1 Noetic

## Clone the project

Clone into the `src` directory of a catkin workspace, including the simulator submodule:

```bash
mkdir -p ~/artpark_ws/src
cd ~/artpark_ws/src

git clone --recurse-submodules \
  https://github.com/YOUR_USERNAME/ArtPark-Intern-Project-Ros1-Noetic.git
```

If you already cloned the repository without submodules, run inside it:

```bash
git submodule update --init --recursive
```

## Install dependencies and build

With ROS 1 Noetic and rosdep installed:

```bash
source /opt/ros/noetic/setup.bash
cd ~/artpark_ws

rosdep install --from-paths src --ignore-src -r -y
catkin_make
source devel/setup.bash
```

In every new terminal used to run the project:

```bash
source /opt/ros/noetic/setup.bash
source ~/artpark_ws/devel/setup.bash
```