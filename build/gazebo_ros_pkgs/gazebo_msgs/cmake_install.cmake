# Install script for directory: /home/caio/catkin_ws/src/gazebo_ros_pkgs/gazebo_msgs

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/caio/catkin_ws/install")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/gazebo_msgs/msg" TYPE FILE FILES
    "/home/caio/catkin_ws/src/gazebo_ros_pkgs/gazebo_msgs/msg/ContactsState.msg"
    "/home/caio/catkin_ws/src/gazebo_ros_pkgs/gazebo_msgs/msg/ContactState.msg"
    "/home/caio/catkin_ws/src/gazebo_ros_pkgs/gazebo_msgs/msg/LinkState.msg"
    "/home/caio/catkin_ws/src/gazebo_ros_pkgs/gazebo_msgs/msg/LinkStates.msg"
    "/home/caio/catkin_ws/src/gazebo_ros_pkgs/gazebo_msgs/msg/ModelState.msg"
    "/home/caio/catkin_ws/src/gazebo_ros_pkgs/gazebo_msgs/msg/ModelStates.msg"
    "/home/caio/catkin_ws/src/gazebo_ros_pkgs/gazebo_msgs/msg/ODEJointProperties.msg"
    "/home/caio/catkin_ws/src/gazebo_ros_pkgs/gazebo_msgs/msg/ODEPhysics.msg"
    "/home/caio/catkin_ws/src/gazebo_ros_pkgs/gazebo_msgs/msg/WorldState.msg"
    )
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/gazebo_msgs/srv" TYPE FILE FILES
    "/home/caio/catkin_ws/src/gazebo_ros_pkgs/gazebo_msgs/srv/ApplyBodyWrench.srv"
    "/home/caio/catkin_ws/src/gazebo_ros_pkgs/gazebo_msgs/srv/DeleteModel.srv"
    "/home/caio/catkin_ws/src/gazebo_ros_pkgs/gazebo_msgs/srv/DeleteLight.srv"
    "/home/caio/catkin_ws/src/gazebo_ros_pkgs/gazebo_msgs/srv/GetLinkState.srv"
    "/home/caio/catkin_ws/src/gazebo_ros_pkgs/gazebo_msgs/srv/GetPhysicsProperties.srv"
    "/home/caio/catkin_ws/src/gazebo_ros_pkgs/gazebo_msgs/srv/SetJointProperties.srv"
    "/home/caio/catkin_ws/src/gazebo_ros_pkgs/gazebo_msgs/srv/SetModelConfiguration.srv"
    "/home/caio/catkin_ws/src/gazebo_ros_pkgs/gazebo_msgs/srv/SpawnModel.srv"
    "/home/caio/catkin_ws/src/gazebo_ros_pkgs/gazebo_msgs/srv/ApplyJointEffort.srv"
    "/home/caio/catkin_ws/src/gazebo_ros_pkgs/gazebo_msgs/srv/GetJointProperties.srv"
    "/home/caio/catkin_ws/src/gazebo_ros_pkgs/gazebo_msgs/srv/GetModelProperties.srv"
    "/home/caio/catkin_ws/src/gazebo_ros_pkgs/gazebo_msgs/srv/GetWorldProperties.srv"
    "/home/caio/catkin_ws/src/gazebo_ros_pkgs/gazebo_msgs/srv/SetLinkProperties.srv"
    "/home/caio/catkin_ws/src/gazebo_ros_pkgs/gazebo_msgs/srv/SetModelState.srv"
    "/home/caio/catkin_ws/src/gazebo_ros_pkgs/gazebo_msgs/srv/BodyRequest.srv"
    "/home/caio/catkin_ws/src/gazebo_ros_pkgs/gazebo_msgs/srv/GetLinkProperties.srv"
    "/home/caio/catkin_ws/src/gazebo_ros_pkgs/gazebo_msgs/srv/GetModelState.srv"
    "/home/caio/catkin_ws/src/gazebo_ros_pkgs/gazebo_msgs/srv/JointRequest.srv"
    "/home/caio/catkin_ws/src/gazebo_ros_pkgs/gazebo_msgs/srv/SetLinkState.srv"
    "/home/caio/catkin_ws/src/gazebo_ros_pkgs/gazebo_msgs/srv/SetPhysicsProperties.srv"
    "/home/caio/catkin_ws/src/gazebo_ros_pkgs/gazebo_msgs/srv/SetJointTrajectory.srv"
    "/home/caio/catkin_ws/src/gazebo_ros_pkgs/gazebo_msgs/srv/GetLightProperties.srv"
    "/home/caio/catkin_ws/src/gazebo_ros_pkgs/gazebo_msgs/srv/SetLightProperties.srv"
    )
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/gazebo_msgs/cmake" TYPE FILE FILES "/home/caio/catkin_ws/build/gazebo_ros_pkgs/gazebo_msgs/catkin_generated/installspace/gazebo_msgs-msg-paths.cmake")
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include" TYPE DIRECTORY FILES "/home/caio/catkin_ws/devel/include/gazebo_msgs")
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/roseus/ros" TYPE DIRECTORY FILES "/home/caio/catkin_ws/devel/share/roseus/ros/gazebo_msgs")
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/common-lisp/ros" TYPE DIRECTORY FILES "/home/caio/catkin_ws/devel/share/common-lisp/ros/gazebo_msgs")
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/gennodejs/ros" TYPE DIRECTORY FILES "/home/caio/catkin_ws/devel/share/gennodejs/ros/gazebo_msgs")
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  execute_process(COMMAND "/usr/bin/python" -m compileall "/home/caio/catkin_ws/devel/lib/python2.7/dist-packages/gazebo_msgs")
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/python2.7/dist-packages" TYPE DIRECTORY FILES "/home/caio/catkin_ws/devel/lib/python2.7/dist-packages/gazebo_msgs")
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pkgconfig" TYPE FILE FILES "/home/caio/catkin_ws/build/gazebo_ros_pkgs/gazebo_msgs/catkin_generated/installspace/gazebo_msgs.pc")
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/gazebo_msgs/cmake" TYPE FILE FILES "/home/caio/catkin_ws/build/gazebo_ros_pkgs/gazebo_msgs/catkin_generated/installspace/gazebo_msgs-msg-extras.cmake")
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/gazebo_msgs/cmake" TYPE FILE FILES
    "/home/caio/catkin_ws/build/gazebo_ros_pkgs/gazebo_msgs/catkin_generated/installspace/gazebo_msgsConfig.cmake"
    "/home/caio/catkin_ws/build/gazebo_ros_pkgs/gazebo_msgs/catkin_generated/installspace/gazebo_msgsConfig-version.cmake"
    )
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/gazebo_msgs" TYPE FILE FILES "/home/caio/catkin_ws/src/gazebo_ros_pkgs/gazebo_msgs/package.xml")
endif()

