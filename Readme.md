# ArtPark ROS Project

This repository contains:

| Folder | Purpose |
|---|---|
| `artpark` | Project package |
| `my_robot_description` | Robot description package |
| `nexus_4wd_mecanum_simulator` | Simulator, tracked as a Git submodule pointing to our fork |

## 1. Clone the project

Clone with submodules to download all three folders:

```bash
git clone --recurse-submodules https://github.com/YOUR_USERNAME/YOUR_MAIN_REPO.git
cd YOUR_MAIN_REPO
```

If you already cloned without submodules, run from the main repository:

```bash
git submodule update --init --recursive
```

## 2. Build the ROS workspace

Use the ROS distribution required by the packages.

If this repository is inside your workspace's `src` folder, return to the workspace root before installing dependencies and building.

For a ROS 2 workspace:

```bash
source /opt/ros/<your_ros_distribution>/setup.bash
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
source install/setup.bash
```

For a ROS 1 catkin workspace:

```bash
source /opt/ros/<your_ros_distribution>/setup.bash
rosdep install --from-paths src --ignore-src -r -y
catkin_make
source devel/setup.bash
```

Run only the commands matching this project's ROS version. Replace `<your_ros_distribution>` before running.

## 3. Update your local project

First commit or stash any local changes, including changes inside the simulator.

From the main repository:

```bash
git pull --ff-only
git submodule update --init --recursive
```

This checks out the simulator commit recorded by the main repository.

## 4. Modify the main project packages

Changes inside `artpark` and `my_robot_description` are committed from the main repository:

```bash
git add artpark my_robot_description
git diff --cached --stat
git commit -m "Update project packages"
git push
```

## 5. Modify the simulator

The simulator has its own Git history. Commit and push simulator changes inside its folder first.

A fresh submodule checkout normally has a detached HEAD. Create a branch before editing:

```bash
cd nexus_4wd_mecanum_simulator
git switch -c simulator-update
```

After making your changes:

```bash
git status
git add .
git diff --cached --stat
git commit -m "Update simulator"
git push -u origin simulator-update
```

Use a unique branch name for each new task. If your working branch already exists locally, switch to it with `git switch <branch-name>`.

Then record the new simulator commit in the main repository:

```bash
cd ..
git add nexus_4wd_mecanum_simulator
git commit -m "Update simulator reference"
git push
```

Always push the simulator commit before pushing the main repository's updated reference. Collaborators need access to both repositories.

## 6. Check repository status

From the main repository:

```bash
git status
git submodule status
git -C nexus_4wd_mecanum_simulator status
```

The main repository records a specific simulator commit. Uncommitted changes inside the simulator are not included in a main-repository commit.