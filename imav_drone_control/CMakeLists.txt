cmake_minimum_required(VERSION 2.8.3)

project(imav_drone_control)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
)

catkin_package()
 
include_directories(${catkin_INCLUDE_DIRS})
 
add_executable(quadrado src/quadrado.cpp)
add_dependencies(quadrado imav_drone_control_generate_messages_cpp)
target_link_libraries(quadrado ${catkin_LIBRARIES})

#add_executable(grid_search src/grid_search.cpp)
#add_dependencies(grid_search imav_drone_control_generate_messages_cpp)
#target_link_libraries(grid_search ${catkin_LIBRARIES})

add_executable(control.cpp src/control.cpp)
add_dependencies(control.cpp imav_drone_control_generate_messages_cpp)
target_link_libraries(control.cpp ${catkin_LIBRARIES})

add_executable(battery src/battery.cpp)
add_dependencies(battery imav_drone_control_generate_messages_cpp)
target_link_libraries(battery ${catkin_LIBRARIES})

add_executable(Delivery src/Delivery.cpp)
add_dependencies(Delivery imav_drone_control_generate_messages_cpp)
target_link_libraries(Delivery ${catkin_LIBRARIES})
