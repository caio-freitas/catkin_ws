
#include <stdlib.h>
#include "math.h"
#include <ros/ros.h>
#include <geometry_msgs/PoseStamped.h>
#include <mavros_msgs/CommandBool.h>
#include <mavros_msgs/SetMode.h>
#include <mavros_msgs/State.h>

#define ERROR 0.5
#define ERROR_ALTITUDE 0.2
/* O pacote "mavros_msgS" contém todas as mensagens necessárias para o funcionamento dos "services" e dos "topics" oriundos do pacote MAVROS. Todos os serviços e tópicos, assim como seus respectivos tipos de mensagens, estão documentados na MAVROS wiki. */

float position_now[3];

mavros_msgs::State current_state;
void state_cb(const mavros_msgs::State::ConstPtr& msg){
    current_state = *msg;
}
/*Criamos uma simples função que salva o estado momentâneo do vôo. Ela nos permite checar parâmetros como: connection, arming e offboard flags. */

void callback_fcu_pose(const geometry_msgs::PoseStamped msg)
{
	//ROS_INFO ("Got data: %f, %f, %f \n", msg.pose.position.x, msg.pose.position.y, msg.pose.position.z );

	position_now[0] =  msg.pose.position.x;
	position_now[1] =  msg.pose.position.y;
	position_now[2] =  msg.pose.position.z;
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
        
        ros::spinOnce();
        rate.sleep();

       if ( (fabs(position_now[0] - goal_x) < ERROR) && fabs(position_now[1] - goal_y) < ERROR && fabs(position_now[2] - goal_z) < ERROR_ALTITUDE)
           break;
    }    
}

void return_to_home(){

    ros::NodeHandle nh;

    ros::Publisher local_pos_pub = nh.advertise<geometry_msgs::PoseStamped>
            ("mavros/setpoint_position/local", 10);

    ros::Rate rate(20.0);

    geometry_msgs::PoseStamped pose;

    printf("\n [ INFO ] Returning to home");

    while(position_now[0] != 0.0 && position_now[1] != 0.0){

    	printf("\n [ INFO ] Returning to home");

        pose.pose.position.x = 0.0;
        pose.pose.position.y = 0.0;
        pose.pose.position.z = altura_desejada;
    
        local_pos_pub.publish(pose);
	ros::spinOnce();
	rate.sleep();
	}        
    while(position_now[2] > 0.3) {
	pose.pose.position.z = -1.0;
	local_pos_pub.publish(pose);
	ros::spinOnce();
	rate.sleep();	
}
        ros::spinOnce();
        rate.sleep();

       if ( (fabs(position_now[0] - 0.0) < ERROR) && fabs(position_now[1] - 0.0) < ERROR && fabs(position_now[2] - 0.0) < ERROR_ALTITUDE){
        
           printf("\n [ INFO ] Mission done successfully :)\n");
           exit(0);
       }
    }    

}


int main(int argc, char **argv)
{

    double altitude_desejada = 10.0;

    printf("\n [ INFO ] Starting IMAV 2019 Searching packages (Skyrats)");
    printf("\n [ INFO ] Powered by Amigos da Poli, Politecnica-USP and CITI");

    ros::init(argc, argv, "SP_Mission_Control");

    ros::NodeHandle nh;

    ros::Subscriber state_sub = nh.subscribe<mavros_msgs::State>
            ("mavros/state", 10, state_cb);

    ros::Subscriber pega_pose = nh.subscribe<geometry_msgs::PoseStamped>
            ("mavros/local_position/pose", 10, callback_fcu_pose);

    ros::Publisher local_pos_pub = nh.advertise<geometry_msgs::PoseStamped>
            ("mavros/setpoint_position/local", 10);

    ros::ServiceClient arming_client = nh.serviceClient<mavros_msgs::CommandBool>
            ("mavros/cmd/arming");

    ros::ServiceClient set_mode_client = nh.serviceClient<mavros_msgs::SetMode>
            ("mavros/set_mode");

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

	else {
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

	//Condicional para checar se o drone decolou!
	if( fabs(position_now[2] - altitude_desejada) < ERROR ){

        printf("\n [ WARN ] Skyrats MAV Takeoff ");

        set_position(10.0, 0.0, altitude_desejada);

        set_position(10.0, 2.0, altitude_desejada);

        set_position(0.0, 2.0, altitude_desejada);

        set_position(0.0, 4.0, altitude_desejada);

        set_position(10.0, 4.0, altitude_desejada);

        set_position(10.0, 6.0, altitude_desejada);	

        set_position(0.0, 6.0, altitude_desejada);

        set_position(0.0, 8.0, altitude_desejada);

        set_position(10.0, 8.0, altitude_desejada);

		set_position(10.0, 10.0, altitude_desejada);

		set_position(0.0, 10.0, altitude_desejada);  
		
		set_position(0.0, 0.0, altitude_desejada);      

// Returning to Home
        return_to_home();

    }  //fim do if verificador de takeoff

	ros::spinOnce();
	rate.sleep();

    }

    return 0;
}
