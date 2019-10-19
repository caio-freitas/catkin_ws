#include <ros/ros.h>
#include <sensor_msgs/BatteryState.h>

double percent;

void battery_callback(const sensor_msgs::BatteryState bat) {
	percent = bat.percentage;
}

int main (int arg, char **argv) {
	ros::init(arg, argv, "battery");
	ros::NodeHandle nh;
	ros::Rate rate(20.0);

	ros::Subscriber battery_sub = nh.subscribe<sensor_msgs::BatteryState>
		("mavros/battery", 1, battery_callback);\

	while(true) {
		printf("%f\n", percent);
		ros::spinOnce();
		rate.sleep();
	}
	return 0;
}
