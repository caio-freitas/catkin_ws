#include <stdlib.h>
#include "math.h"
#include <ros/ros.h>
#include <std_msgs/String.h>
#include <std_msgs/Bool.h>
#include <geometry_msgs/PoseStamped.h>
#include <mavros_msgs/CommandBool.h>
#include <mavros_msgs/SetMode.h>
#include <mavros_msgs/State.h>
#include <geometry_msgs/TwistStamped.h>
#include <mavros_msgs/GlobalPositionTarget.h>
#include <mavros_msgs/CommandHome.h>
#include <sensor_msgs/NavSatFix.h>

#define GPS_ERROR 0.000001
#define ERROR 0.5
#define ERROR_ALTITUDE 0.3
/* O pacote "mavros_msgS" contém todas as mensagens necessárias para o funcionamento dos "services" e dos "topics" oriundos do pacote MAVROS. Todos os serviços e tópicos, assim como seus respectivos tipos de mensagens, estão documentados na MAVROS wiki. */

float position_now[3];

mavros_msgs::State current_state;

bool interrupt_message;
bool node_message;
bool aligned_message;

geometry_msgs::TwistStamped twist;

sensor_msgs::NavSatFix gps_pose;
sensor_msgs::NavSatFix HOME_POSITION;
sensor_msgs::NavSatFix SEARCH_POSITION;
/****************** Search Position Setup ********************/



void state_cb(const mavros_msgs::State::ConstPtr& msg){
    current_state = *msg;
}
/*Criamos uma simples função que salva o estado momentâneo do vôo. Ela nos permite checar parâmetros como: connection, arming e offboard flags. */

void callback_fcu_pose(const geometry_msgs::PoseStamped msg)
{
	//printf ("Got data: %f, %f, %f \n", msg.pose.position.x, msg.pose.position.y, msg.pose.position.z );

	position_now[0] =  msg.pose.position.x;
	position_now[1] =  msg.pose.position.y;
	position_now[2] =  msg.pose.position.z;
}

void callback_fcu_interrompe(const std_msgs::Bool mensagem)
{
	interrupt_message = mensagem.data;
}

void callback_fcu_node(const std_msgs::Bool mensagem)
{
	node_message = mensagem.data;
}

void callback_fcu_aligned(const std_msgs::Bool mensagem)
{
	aligned_message = mensagem.data;
}

// TESTAR GPS ERROR
void go_to_global_pose(double latitude, double longitude, double change_height) {
  ros::NodeHandle nh;
  ros::Rate rate(20.0);
  ros::Publisher gps_pos_pub = nh.advertise<mavros_msgs::GlobalPositionTarget>
          ("mavros/setpoint_position/global", 10);

  mavros_msgs::GlobalPositionTarget g_pose;
  g_pose.latitude = latitude;
  g_pose.longitude = longitude;
  g_pose.altitude = gps_pose.altitude + change_height; //Mantenha a altitude atual, some change_height
  while (((gps_pose.latitude - g_pose.latitude) > GPS_ERROR) && ((gps_pose.longitude - g_pose.longitude) > GPS_ERROR)) {
    gps_pos_pub.publish(g_pose);
    rate.sleep();
  }
}

// REFEITO
void return_to_home(){

    ros::NodeHandle nh;

    ros::Publisher local_pos_pub = nh.advertise<geometry_msgs::PoseStamped>
            ("mavros/setpoint_position/local", 10);

    ros::Publisher vel_pos_pub = nh.advertise<geometry_msgs::TwistStamped>
                ("mavros/setpoint_velocity/cmd_vel", 10);

    ros::ServiceClient arming_client = nh.serviceClient<mavros_msgs::CommandBool>
                ("mavros/cmd/arming");

    ros::Rate rate(20.0);

    geometry_msgs::PoseStamped pose;

    geometry_msgs::TwistStamped twist;

    mavros_msgs::CommandBool arm_cmd;
    printf("%f - %f", gps_pose.latitude, HOME_POSITION.latitude);
    while (abs(gps_pose.latitude - HOME_POSITION.latitude) > GPS_ERROR || abs(gps_pose.longitude - HOME_POSITION.longitude) > GPS_ERROR) {
      printf("Returning to home!");
      go_to_global_pose(HOME_POSITION.latitude, HOME_POSITION.longitude, 0);
    }
    printf("%f", position_now[2]);
    while (position_now[2] > 0) {
      printf("It's going down!");
      twist.twist.linear.x = 0;
      twist.twist.linear.y = 0;
      twist.twist.linear.z = -1;

      vel_pos_pub.publish(twist);

      ros::spinOnce();
      rate.sleep();
    }

    //mavros_msgs::CommandBool arm_cmd;
    arm_cmd.request.value = true;
    arming_client.call(arm_cmd);

    printf("Mission executed successfully ;)");
    for(int i=0; i < 3333; i++) {
      printf("VOA SKYRATS  ");
      arming_client.call(arm_cmd);
    }
    exit(0);
}

// ANALIZAR
void delivery_package(){

	ros::NodeHandle nh;
	ros::Publisher vel_pos_pub = nh.advertise<geometry_msgs::TwistStamped>
            ("mavros/setpoint_velocity/cmd_vel", 10);
  ros::Rate rate(20.0);

	//desce um pouco
	while(fabs(position_now[2] - 1.0) > ERROR_ALTITUDE){

		printf("[ INFO ] Flying down to delivery the package.");

		twist.twist.linear.x = 0.0;
		twist.twist.linear.y = 0.0;
		twist.twist.linear.z = -1.0;

		vel_pos_pub.publish(twist);

		ros::spinOnce();
		rate.sleep();

	}

	//abre a garra
	printf("[ INFO ] Robotic Claw opening.");
	system("./abrir_garra.sh");

	//sobe mais um pouco por segurança
	while(fabs(position_now[2] - 4.0) > ERROR_ALTITUDE){

		printf("[ INFO ] Flying up to return to home.");

		twist.twist.linear.x = 0.0;
		twist.twist.linear.y = 0.0;
		twist.twist.linear.z = 1.0;

		vel_pos_pub.publish(twist);
		ros::spinOnce();
		rate.sleep();

	}

	//volta pra casa
	return_to_home();
}

// PEGAR VERIFICATION DO COLOMBINI (OU NAO)
void verification(){

  ros::NodeHandle nh;

	if(interrupt_message == 1){
    printf("\n [ WARN ] Mission interrupted. Returning to home.");


		return_to_home();
	}

	while(node_message == 1){

		printf("\n [ WARN ] Mission interrupted. Drone trying to align.");

		if(aligned_message == 1){

			//delivery_package();
		}
	}
}

void set_position(double goal_x, double goal_y, double goal_z){

    ros::NodeHandle nh;

    ros::Publisher local_pos_pub = nh.advertise<geometry_msgs::PoseStamped>
            ("mavros/setpoint_position/local", 10);

    ros::Rate rate(20.0);
    geometry_msgs::PoseStamped pose;

    printf("\n [ INFO ] Going to position (%f, %f,%f)", goal_x, goal_y, goal_z);

    while(position_now[0] != goal_x && position_now[1] != goal_y && position_now[2] != goal_z){

    	printf("\n [ INFO ] Local position: (%f, %f, %f)", position_now[0], position_now[1], position_now[2]);

        pose.pose.position.x = goal_x;
        pose.pose.position.y = goal_y;
        pose.pose.position.z = goal_z;

        local_pos_pub.publish(pose);

        verification();

        ros::spinOnce();
        rate.sleep();

       if ( (fabs(position_now[0] - goal_x) < ERROR) && fabs(position_now[1] - goal_y) < ERROR && fabs(position_now[2] - goal_z) < ERROR_ALTITUDE)
           break;
    }
}
//<sensor_msgs/NavSatFix.h>
void gps_callback(const sensor_msgs::NavSatFix msg){
    gps_pose = msg;
    //ROS_INFO("GPS Position: (%f, %f)", gps_pose.latitude, gps_pose.longitude);
}

int main(int argc, char **argv)
{
	double altitude_desejada = 4.0;
  double r = altitude_desejada*sin(51* 	3.14159265358979323846/180);
  double step = 1.5*r;

  SEARCH_POSITION.latitude = -23.556028;
  SEARCH_POSITION.longitude = -46.7302808;

  printf("\n [ INFO ] Starting IMAV 2019 Delivery Packages mission (Skyrats)");
  printf("\n [ INFO ] Powered by Amigos da Poli, Politecnica-USP and CITI");

  ros::init(argc, argv, "Madrid_Mission_Control");

  ros::NodeHandle nh;

  ros::Subscriber gps_sub = nh.subscribe<sensor_msgs::NavSatFix>
            ("/mavros/global_position/global", 10, gps_callback);

  ros::Subscriber state_sub = nh.subscribe<mavros_msgs::State>
            ("mavros/state", 10, state_cb);

  ros::Subscriber pega_pose = nh.subscribe<geometry_msgs::PoseStamped>
            ("mavros/local_position/pose", 10, callback_fcu_pose);

  ros::Subscriber interrompe = nh.subscribe<std_msgs::Bool>
            ("interrompe", 1, callback_fcu_interrompe);

  ros::Subscriber node = nh.subscribe<std_msgs::Bool>
            ("pack/node", 10, callback_fcu_node);

  ros::Subscriber aligned = nh.subscribe<std_msgs::Bool>
            ("pack/aligned", 10, callback_fcu_aligned);

  ros::Publisher local_pos_pub = nh.advertise<geometry_msgs::PoseStamped>
            ("mavros/setpoint_position/local", 10);

  ros::ServiceClient arming_client = nh.serviceClient<mavros_msgs::CommandBool>
            ("mavros/cmd/arming");

  ros::ServiceClient set_mode_client = nh.serviceClient<mavros_msgs::SetMode>

            ("mavros/set_mode");

  ros::ServiceClient set_home = nh.serviceClient<mavros_msgs::CommandHome>
            ("mavros/cmd/set_home");

    /*Acima, instanciamos um "publisher" a fim de publicar a posição da aeronave, bem como "clients" apropriedades, de forma a dar o comando "arm".*/

    //the setpoint publishing rate MUST be faster than 2Hz
  ros::Rate rate(20.0);

    /* A pilha de vôo do PX4 possui um intervalo de 500ms entre dois comandos offboard. Se esse intervalo for excedido, o programa de comando irá voltar para o último estado da aeronave antes de entrar no modo offboard! */

  while(ros::ok() && !current_state.connected){

      printf("\n [ INFO ] Waiting for connection");
      ros::spinOnce();
      rate.sleep();
  }

	/* Antes de publicarmos algo, nós esperamos a conexão a ser estabelecida entre a MAVROS e o autopilot. Esse loop se encerrará quando a mensagem for recebida! */

  geometry_msgs::PoseStamped pose;

  pose.pose.position.x = 0;
  pose.pose.position.y = 0;
  pose.pose.position.z = 0;

    //send a few setpoints before starting

  for(int i = 100; ros::ok() && i > 0; --i){
      local_pos_pub.publish(pose);

      ros::spinOnce();

      rate.sleep();
  }

  /* Antes de entrarmos no modo offboard, você tem que ter iniciado os setpoints de transmissão. Caso contrário, a escolha do modo de vôo será rejeitada (próx. passo). Aqui, o número 100 foi uma escolha arbitrária */

  mavros_msgs::SetMode offb_set_mode;
  offb_set_mode.request.custom_mode = "OFFBOARD";

  node_message = 0;

  mavros_msgs::CommandBool arm_cmd;
  arm_cmd.request.value = true;

  ros::Time last_request = ros::Time::now();

  pose.pose.position.x = 0.0;
  pose.pose.position.y = 0.0;
  pose.pose.position.z = altitude_desejada;

  local_pos_pub.publish(pose);


  while(ros::ok()){

    if( current_state.mode != "OFFBOARD" &&
              (ros::Time::now() - last_request > ros::Duration(5.0))){
              if( set_mode_client.call(offb_set_mode) &&
                  offb_set_mode.response.mode_sent){
                  ROS_INFO("\n[ INFO ] Offboard enabled");
              }
              last_request = ros::Time::now();
          }

   else { printf("else\n");
              if( !current_state.armed &&
                  (ros::Time::now() - last_request > ros::Duration(5.0))){
                  if( arming_client.call(arm_cmd) &&
                      arm_cmd.response.success){
                      ROS_INFO("\n[ WARN ] Skyrats MAV armed");
                  }
                  last_request = ros::Time::now();
              }
          }


	local_pos_pub.publish(pose);


  HOME_POSITION = gps_pose;

	//Condicional para checar se o drone decolou!
  printf("%f\n",position_now[2]);
	if (fabs(position_now[2] - altitude_desejada) < ERROR){
    //while ()
        ROS_WARN("Skyrats MAV Takeoff!\n");
        /*********** goas to search position and sets as home **********/
        go_to_global_pose(SEARCH_POSITION.latitude, SEARCH_POSITION.longitude, 0);

      mavros_msgs::CommandHome NEW_HOME;
      NEW_HOME.request.latitude = gps_pose.latitude;
      NEW_HOME.request.longitude = gps_pose.longitude;
      NEW_HOME.request.altitude = HOME_POSITION.altitude;
      set_home.call(NEW_HOME);
        /****************************************/
    for(double s = 0; (s <= 10); s += step)
        set_position(s, 0.0, altitude_desejada);
        //for(s = 0; (s <= 2); s += step)
    set_position(10.0, 2.0, altitude_desejada);

    set_position(0.0,  2.0, altitude_desejada);

    set_position(0.0,  4.0, altitude_desejada);

    set_position(10.0, 4.0, altitude_desejada);

    set_position(10.0, 6.0, altitude_desejada);

    set_position(0.0,  6.0, altitude_desejada);

    set_position(0.0,  8.0, altitude_desejada);

    set_position(10.0, 8.0, altitude_desejada);

    set_position(10.0, 10.0, altitude_desejada);

		set_position(0.0,  10.0, altitude_desejada);

		set_position(0.0,   0.0, altitude_desejada);

		// Returning to Home
        return_to_home();
	 printf("[ INFO ] Robotic Claw opening.");
        system("./abrir_garra.sh");

      }
      //fim do if verificador de takeoff

	ros::spinOnce();
	rate.sleep();
}
  return 0;

  }
