cmake_minimum_required(VERSION 3.0.2)
project(my_robot_description)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  gazebo_ros
  geometry_msgs
)

find_package(gazebo REQUIRED)

catkin_package()

include_directories(
  ${catkin_INCLUDE_DIRS}
  ${GAZEBO_INCLUDE_DIRS}
)

# Add the plugin
add_library(pose_publisher_plugin SHARED
  src/pose_publisher_plugin.cc
)

# Install the plugin
install(TARGETS pose_publisher_plugin
  LIBRARY DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
)

target_link_libraries(pose_publisher_plugin
  ${catkin_LIBRARIES}
  ${GAZEBO_LIBRARIES}
)
