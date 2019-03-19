// Generated by gencpp from file mavros_msgs/HilActuatorControls.msg
// DO NOT EDIT!


#ifndef MAVROS_MSGS_MESSAGE_HILACTUATORCONTROLS_H
#define MAVROS_MSGS_MESSAGE_HILACTUATORCONTROLS_H


#include <string>
#include <vector>
#include <map>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>

#include <std_msgs/Header.h>

namespace mavros_msgs
{
template <class ContainerAllocator>
struct HilActuatorControls_
{
  typedef HilActuatorControls_<ContainerAllocator> Type;

  HilActuatorControls_()
    : header()
    , controls()
    , mode(0)
    , flags(0)  {
      controls.assign(0.0);
  }
  HilActuatorControls_(const ContainerAllocator& _alloc)
    : header(_alloc)
    , controls()
    , mode(0)
    , flags(0)  {
  (void)_alloc;
      controls.assign(0.0);
  }



   typedef  ::std_msgs::Header_<ContainerAllocator>  _header_type;
  _header_type header;

   typedef boost::array<float, 16>  _controls_type;
  _controls_type controls;

   typedef uint8_t _mode_type;
  _mode_type mode;

   typedef uint64_t _flags_type;
  _flags_type flags;





  typedef boost::shared_ptr< ::mavros_msgs::HilActuatorControls_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::mavros_msgs::HilActuatorControls_<ContainerAllocator> const> ConstPtr;

}; // struct HilActuatorControls_

typedef ::mavros_msgs::HilActuatorControls_<std::allocator<void> > HilActuatorControls;

typedef boost::shared_ptr< ::mavros_msgs::HilActuatorControls > HilActuatorControlsPtr;
typedef boost::shared_ptr< ::mavros_msgs::HilActuatorControls const> HilActuatorControlsConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::mavros_msgs::HilActuatorControls_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::mavros_msgs::HilActuatorControls_<ContainerAllocator> >::stream(s, "", v);
return s;
}

} // namespace mavros_msgs

namespace ros
{
namespace message_traits
{



// BOOLTRAITS {'IsFixedSize': False, 'IsMessage': True, 'HasHeader': True}
// {'geographic_msgs': ['/opt/ros/kinetic/share/geographic_msgs/cmake/../msg'], 'sensor_msgs': ['/opt/ros/kinetic/share/sensor_msgs/cmake/../msg'], 'std_msgs': ['/opt/ros/kinetic/share/std_msgs/cmake/../msg'], 'mavros_msgs': ['/home/caio/catkin_ws/src/mavros/mavros_msgs/msg'], 'geometry_msgs': ['/opt/ros/kinetic/share/geometry_msgs/cmake/../msg'], 'uuid_msgs': ['/opt/ros/kinetic/share/uuid_msgs/cmake/../msg']}

// !!!!!!!!!!! ['__class__', '__delattr__', '__dict__', '__doc__', '__eq__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_parsed_fields', 'constants', 'fields', 'full_name', 'has_header', 'header_present', 'names', 'package', 'parsed_fields', 'short_name', 'text', 'types']




template <class ContainerAllocator>
struct IsFixedSize< ::mavros_msgs::HilActuatorControls_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::mavros_msgs::HilActuatorControls_<ContainerAllocator> const>
  : FalseType
  { };

template <class ContainerAllocator>
struct IsMessage< ::mavros_msgs::HilActuatorControls_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::mavros_msgs::HilActuatorControls_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::mavros_msgs::HilActuatorControls_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::mavros_msgs::HilActuatorControls_<ContainerAllocator> const>
  : TrueType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::mavros_msgs::HilActuatorControls_<ContainerAllocator> >
{
  static const char* value()
  {
    return "18482e8ef0330ac2fc9a0421be1d11c3";
  }

  static const char* value(const ::mavros_msgs::HilActuatorControls_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0x18482e8ef0330ac2ULL;
  static const uint64_t static_value2 = 0xfc9a0421be1d11c3ULL;
};

template<class ContainerAllocator>
struct DataType< ::mavros_msgs::HilActuatorControls_<ContainerAllocator> >
{
  static const char* value()
  {
    return "mavros_msgs/HilActuatorControls";
  }

  static const char* value(const ::mavros_msgs::HilActuatorControls_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::mavros_msgs::HilActuatorControls_<ContainerAllocator> >
{
  static const char* value()
  {
    return "# HilActuatorControls.msg\n\
#\n\
# ROS representation of MAVLink HIL_ACTUATOR_CONTROLS\n\
# See mavlink message documentation here:\n\
# https://pixhawk.ethz.ch/mavlink/#HIL_ACTUATOR_CONTROLS\n\
\n\
std_msgs/Header header\n\
float32[16] controls\n\
uint8 mode\n\
uint64 flags\n\
\n\
================================================================================\n\
MSG: std_msgs/Header\n\
# Standard metadata for higher-level stamped data types.\n\
# This is generally used to communicate timestamped data \n\
# in a particular coordinate frame.\n\
# \n\
# sequence ID: consecutively increasing ID \n\
uint32 seq\n\
#Two-integer timestamp that is expressed as:\n\
# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')\n\
# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')\n\
# time-handling sugar is provided by the client library\n\
time stamp\n\
#Frame this data is associated with\n\
# 0: no frame\n\
# 1: global frame\n\
string frame_id\n\
";
  }

  static const char* value(const ::mavros_msgs::HilActuatorControls_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::mavros_msgs::HilActuatorControls_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.header);
      stream.next(m.controls);
      stream.next(m.mode);
      stream.next(m.flags);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct HilActuatorControls_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::mavros_msgs::HilActuatorControls_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::mavros_msgs::HilActuatorControls_<ContainerAllocator>& v)
  {
    s << indent << "header: ";
    s << std::endl;
    Printer< ::std_msgs::Header_<ContainerAllocator> >::stream(s, indent + "  ", v.header);
    s << indent << "controls[]" << std::endl;
    for (size_t i = 0; i < v.controls.size(); ++i)
    {
      s << indent << "  controls[" << i << "]: ";
      Printer<float>::stream(s, indent + "  ", v.controls[i]);
    }
    s << indent << "mode: ";
    Printer<uint8_t>::stream(s, indent + "  ", v.mode);
    s << indent << "flags: ";
    Printer<uint64_t>::stream(s, indent + "  ", v.flags);
  }
};

} // namespace message_operations
} // namespace ros

#endif // MAVROS_MSGS_MESSAGE_HILACTUATORCONTROLS_H
