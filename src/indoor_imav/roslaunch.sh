cd ~/src/Firmware
source ~/catkin_ws/devel/setup.bash    //
source Tools/setup_gazebo.bash $(pwd) $(pwd)/posix_sitl_default
source /opt/ros/kinetic/setup.bash
source /usr/share/gazebo/setup.sh
## linha importante ##
source $HOME/src/Firmware/Tools/setup_gazebo.bash $HOME/src/Firmware $HOME/src/Firmware/build/posix_sitl_default > /dev/null 2>&1
######################
export GAZEBO_PLUGIN_PATH=${GAZEBO_PLUGIN_PATH}:$HOME/src/Firmware/Tools/sitl_gazebo/build
export SITL_GAZEBO_PATH=$HOME/src/Firmware/Tools/sitl_gazebo
export PYTHONPATH=$PYTHONPATH:/usr/lib/python2.7/dist-packages
export ROS_PACKAGE_PATH=$ROS_PACKAGE_PATH:$(pwd)
export ROS_PACKAGE_PATH=$ROS_PACKAGE_PATH:$(pwd)/Tools/sitl_gazebo

#roslaunch px4 posix_sitl.launch
gnome-terminal -x cd ~/src/Firmware/ & roslaunch px4 posix_sitl.launch
roslaunch indoor_imav indoor.launch
