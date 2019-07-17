cmake_minimum_required(VERSION 2.4.6)
project(dso_ros)

find_package(catkin REQUIRED COMPONENTS
  geometry_msgs
  roscpp
  sensor_msgs
  cv_bridge
)

set(DSO_PATH /home/yipuzhao/Codes/VSLAM/DSO)
# set(DSO_PATH $ENV{DSO_PATH})
message("\n\n---- LOOKING FOR DSO at\n\"${DSO_PATH}\"")

set(Pangolin_FOUND TRUE)
set(Pangolin_INCLUDE_DIRS /opt/Pangolin/include/)
set(Pangolin_LIBRARIES /opt/Pangolin/lib/libpangolin.so)
# find_package(Pangolin 0.2 REQUIRED)
message("\n\n---- FOUND Pangolin Headers at\n\"${Pangolin_INCLUDE_DIRS}\"")
message("---- FOUND Pangolin Libs at\n\"${Pangolin_LIBRARIES}\"")

# customize opencv dir
if ($ENV{ROS_DISTRO} STREQUAL "indigo")
    set( OpenCV_DIR /opt/opencv2/share/OpenCV )
    find_package(OpenCV 2.4.13 REQUIRED core ocl)
elseif ($ENV{ROS_DISTRO} STREQUAL "kinetic")
    set( OpenCV_DIR /opt/opencv3/share/OpenCV )
    find_package(OpenCV 3.4.0 REQUIRED)
endif()
# find_package(OpenCV REQUIRED)
message("\n\n---- FOUND OpenCV Headers at\n\"${OpenCV_INCLUDE_DIRS}\"")
message("---- FOUND OpenCV Libs at\n\"${OpenCV_LIBS}\"")

# find_package(Eigen3 REQUIRED)
set( EIGEN3_INCLUDE_DIR /usr/include/eigen3 )
MESSAGE("EIGEN include dir: " ${EIGEN3_INCLUDE_DIR})

find_package(Boost COMPONENTS system thread)

find_library(DSO_LIBRARY dso ${DSO_PATH}/build/lib)

set(GL_LIBRARIES
  GLEW
  GL
)

catkin_package(
  CATKIN_DEPENDS
    geometry_msgs
    roscpp
    sensor_msgs
    cv_bridge
)

###########
## Build ##
###########

set(CMAKE_CXX_FLAGS
   "${SSE_FLAGS} -O2 -g -std=c++0x -march=native -fno-omit-frame-pointer"
)

include_directories(
  ${PROJECT_SOURCE_DIR}/src
  ${DSO_PATH}/src
  ${DSO_PATH}/thirdparty/Sophus
  ${Pangolin_INCLUDE_DIRS}
  ${EIGEN3_INCLUDE_DIR}
  ${catkin_INCLUDE_DIRS}
)

## Declare a C++ executable
add_executable(dso_live src/main.cpp)

target_link_libraries(dso_live
    ${GL_LIBRARIES}
    ${DSO_LIBRARY}
    ${Pangolin_LIBRARIES}
    ${OpenCV_LIBS}
    ${catkin_LIBRARIES})
