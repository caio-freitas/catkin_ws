// Generated by gencpp from file mavros_msgs/Mavlink.msg
// DO NOT EDIT!


#ifndef MAVROS_MSGS_MESSAGE_MAVLINK_H
#define MAVROS_MSGS_MESSAGE_MAVLINK_H


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
struct Mavlink_
{
  typedef Mavlink_<ContainerAllocator> Type;

  Mavlink_()
    : header()
    , framing_status(0)
    , magic(0)
    , len(0)
    , incompat_flags(0)
    , compat_flags(0)
    , seq(0)
    , sysid(0)
    , compid(0)
    , msgid(0)
    , checksum(0)
    , payload64()
    , signature()  {
    }
  Mavlink_(const ContainerAllocator& _alloc)
    : header(_alloc)
    , framing_status(0)
    , magic(0)
    , len(0)
    , incompat_flags(0)
    , compat_flags(0)
    , seq(0)
    , sysid(0)
    , compid(0)
    , msgid(0)
    , checksum(0)
    , payload64(_alloc)
    , signature(_alloc)  {
  (void)_alloc;
    }



   typedef  ::std_msgs::Header_<ContainerAllocator>  _header_type;
  _header_type header;

   typedef uint8_t _framing_status_type;
  _framing_status_type framing_status;

   typedef uint8_t _magic_type;
  _magic_type magic;

   typedef uint8_t _len_type;
  _len_type len;

   typedef uint8_t _incompat_flags_type;
  _incompat_flags_type incompat_flags;

   typedef uint8_t _compat_flags_type;
  _compat_flags_type compat_flags;

   typedef uint8_t _seq_type;
  _seq_type seq;

   typedef uint8_t _sysid_type;
  _sysid_type sysid;

   typedef uint8_t _compid_type;
  _compid_type compid;

   typedef uint32_t _msgid_type;
  _msgid_type msgid;

   typedef uint16_t _checksum_type;
  _checksum_type checksum;

   typedef std::vector<uint64_t, typename ContainerAllocator::template rebind<uint64_t>::other >  _payload64_type;
  _payload64_type payload64;

   typedef std::vector<uint8_t, typename ContainerAllocator::template rebind<uint8_t>::other >  _signature_type;
  _signature_type signature;



  enum {
    FRAMING_OK = 1u,
    FRAMING_BAD_CRC = 2u,
    FRAMING_BAD_SIGNATURE = 3u,
    MAVLINK_V10 = 254u,
    MAVLINK_V20 = 253u,
  };


  typedef boost::shared_ptr< ::mavros_msgs::Mavlink_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::mavros_msgs::Mavlink_<ContainerAllocator> const> ConstPtr;

}; // struct Mavlink_

typedef ::mavros_msgs::Mavlink_<std::allocator<void> > Mavlink;

typedef boost::shared_ptr< ::mavros_msgs::Mavlink > MavlinkPtr;
typedef boost::shared_ptr< ::mavros_msgs::Mavlink const> MavlinkConstPtr;

// constants requiring out of line definition

   

   

   

   

   



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::mavros_msgs::Mavlink_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::mavros_msgs::Mavlink_<ContainerAllocator> >::stream(s, "", v);
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
struct IsFixedSize< ::mavros_msgs::Mavlink_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::mavros_msgs::Mavlink_<ContainerAllocator> const>
  : FalseType
  { };

template <class ContainerAllocator>
struct IsMessage< ::mavros_msgs::Mavlink_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::mavros_msgs::Mavlink_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::mavros_msgs::Mavlink_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::mavros_msgs::Mavlink_<ContainerAllocator> const>
  : TrueType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::mavros_msgs::Mavlink_<ContainerAllocator> >
{
  static const char* value()
  {
    return "41093e1fd0f3eea1da2aa33a177e5ba6";
  }

  static const char* value(const ::mavros_msgs::Mavlink_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0x41093e1fd0f3eea1ULL;
  static const uint64_t static_value2 = 0xda2aa33a177e5ba6ULL;
};

template<class ContainerAllocator>
struct DataType< ::mavros_msgs::Mavlink_<ContainerAllocator> >
{
  static const char* value()
  {
    return "mavros_msgs/Mavlink";
  }

  static const char* value(const ::mavros_msgs::Mavlink_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::mavros_msgs::Mavlink_<ContainerAllocator> >
{
  static const char* value()
  {
    return "# Mavlink message transport type.\n\
#\n\
# Used to transport mavlink_message_t via ROS topic\n\
#\n\
# :framing_status:\n\
#       Frame decoding status: OK, CRC error, bad Signature (mavlink v2.0)\n\
#       You may simply drop all non valid messages.\n\
#       Used for GCS Bridge to transport unknown messages.\n\
#\n\
# :magic:\n\
#       STX byte, used to determine protocol version v1.0 or v2.0.\n\
#\n\
# Please use mavros_msgs::mavlink::convert() from <mavros_msgs/mavlink_convert.h>\n\
# to convert between ROS and MAVLink message type\n\
\n\
# mavlink_framing_t enum\n\
uint8 FRAMING_OK = 1\n\
uint8 FRAMING_BAD_CRC = 2\n\
uint8 FRAMING_BAD_SIGNATURE = 3\n\
\n\
# stx values\n\
uint8 MAVLINK_V10 = 254\n\
uint8 MAVLINK_V20 = 253\n\
\n\
std_msgs/Header header\n\
uint8 framing_status\n\
\n\
uint8 magic		# STX byte\n\
uint8 len\n\
uint8 incompat_flags\n\
uint8 compat_flags\n\
uint8 seq\n\
uint8 sysid\n\
uint8 compid\n\
uint32 msgid		# 24-bit message id\n\
uint16 checksum\n\
uint64[] payload64\n\
uint8[] signature	# optional signature\n\
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

  static const char* value(const ::mavros_msgs::Mavlink_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::mavros_msgs::Mavlink_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.header);
      stream.next(m.framing_status);
      stream.next(m.magic);
      stream.next(m.len);
      stream.next(m.incompat_flags);
      stream.next(m.compat_flags);
      stream.next(m.seq);
      stream.next(m.sysid);
      stream.next(m.compid);
      stream.next(m.msgid);
      stream.next(m.checksum);
      stream.next(m.payload64);
      stream.next(m.signature);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct Mavlink_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::mavros_msgs::Mavlink_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::mavros_msgs::Mavlink_<ContainerAllocator>& v)
  {
    s << indent << "header: ";
    s << std::endl;
    Printer< ::std_msgs::Header_<ContainerAllocator> >::stream(s, indent + "  ", v.header);
    s << indent << "framing_status: ";
    Printer<uint8_t>::stream(s, indent + "  ", v.framing_status);
    s << indent << "magic: ";
    Printer<uint8_t>::stream(s, indent + "  ", v.magic);
    s << indent << "len: ";
    Printer<uint8_t>::stream(s, indent + "  ", v.len);
    s << indent << "incompat_flags: ";
    Printer<uint8_t>::stream(s, indent + "  ", v.incompat_flags);
    s << indent << "compat_flags: ";
    Printer<uint8_t>::stream(s, indent + "  ", v.compat_flags);
    s << indent << "seq: ";
    Printer<uint8_t>::stream(s, indent + "  ", v.seq);
    s << indent << "sysid: ";
    Printer<uint8_t>::stream(s, indent + "  ", v.sysid);
    s << indent << "compid: ";
    Printer<uint8_t>::stream(s, indent + "  ", v.compid);
    s << indent << "msgid: ";
    Printer<uint32_t>::stream(s, indent + "  ", v.msgid);
    s << indent << "checksum: ";
    Printer<uint16_t>::stream(s, indent + "  ", v.checksum);
    s << indent << "payload64[]" << std::endl;
    for (size_t i = 0; i < v.payload64.size(); ++i)
    {
      s << indent << "  payload64[" << i << "]: ";
      Printer<uint64_t>::stream(s, indent + "  ", v.payload64[i]);
    }
    s << indent << "signature[]" << std::endl;
    for (size_t i = 0; i < v.signature.size(); ++i)
    {
      s << indent << "  signature[" << i << "]: ";
      Printer<uint8_t>::stream(s, indent + "  ", v.signature[i]);
    }
  }
};

} // namespace message_operations
} // namespace ros

#endif // MAVROS_MSGS_MESSAGE_MAVLINK_H
