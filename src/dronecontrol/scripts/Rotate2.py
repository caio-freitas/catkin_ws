#!/usr/bin/env python

#Precisamos melhorar, na minha opniao, a questao dos lacos que ficam envinado a posicao e o angulo q ele tem que ficar para nao perder a conexao
#no caso isso envolve uma reeinterpracao dos set_xxx e dos rel_xxx.
#Nao sei ao certo o que fazer, apenas um comentario, talvez eu esteja erado

#blibiotecas
import rospy
import mavros_msgs
from mavros_msgs import srv
from geometry_msgs.msg import PoseStamped, Quaternion
from mavros_msgs.msg import State
import time
import math

#Objetos globais
drone_pose = PoseStamped()
goal_pose = PoseStamped()
drone_state = State()
goal_rotation = Quaternion()
quaternion_axis = [goal_rotation.x = 0, goal_rotation.y = 0, goal_rotation.z = 0]
goal_rotation.w = 1

#Constantes
SECURE = 0.1
    #Marca o a relacao do quaternion na forma de seno e cosseno, sendo constantes (i, j, k)
rotation_axis = [0, 0, 1]


#Funcoes para controle do drone (nomes autoexplicativos)
def secure_accuracy (x,y):
    if (abs(x.pose.position.z - y.pose.position.z) < SECURE) and (abs(x.pose.position.y - y.pose.position.y) < SECURE) and (abs(x.pose.position.x - y.pose.position.x) < SECURE ):
        return True
    return False


def get_orientation():
    global drone_pose
    theta = 360*math.acos(drone_pose.pose.orientation.w)/(math.pi)
#nao vejo utilidade em saber qual a real situacao dos eixos do quaternion, sendo que eles estao em sua maioria imoveis, sendo controlados pela relaco com theta
    #t = (drone_pose.pose.orientation.x/math.sin(theta), drone_pose.pose.orientation.y/math.sin(theta), drone_pose.pose.orientation.z/math.sin(theta))
    return theta, t


def state_callback(state_data):
    global drone_state
    drone_state = state_data


def local_callback(local):
    global drone_pose
    drone_pose = local


def set_position(x, y, z):
    global goal_pose
    global goal_rotation
    goal_pose.pose.position.x = x
    goal_pose.pose.position.y = y
    goal_pose.pose.position.z = z
    goal_pose.pose.orientation = goal_rotation
    local_position_pub.publish(goal_pose)

#Exclui os fatores (x, y, z) porque eles vao ser constates, pois o eixo de rotacao serao sempre o z (0,0,1)
def set_rotation (theta):
    global goal_rotation
    global quaternion_axis
    global rotation_axis
    #nesta conversao de graus para radianos ja e' realizada a divisao por 2 que corrige a rotacao do quaternion
    #pois a conversao correta exige uma divisao por 180 graus, neste caso estamos fazendo ja por 360 (2*180)
    theta = math.pi*theta/360
    #Este if nao e' necessario, o esses fatores serao constantes, sendo o z sempre 1 e o resto 0, para que o drone gira apenas entorno de Z
#    if x*x + y*y + z*z != 1:
#        norm = math.sqrt((x*x) + (y*y) + (z*z))
#        x /= norm
#        y /= norm
#        z /= norm

#    goal_rotation.x = math.sin(theta)*x
#    goal_rotation.y = math.sin(theta)*y
#    goal_rotation.z = math.sin(theta)*z
    quaternion_axis = [ x * math.sin(theta) for x in rotation_axis]
    goal_rotation.w = math.cos(theta)


def rel_position (x, y, z):
    global drone_pose
    x = drone_pose.pose.position.x + x
    y = drone_pose.pose.position.y + y
    z = drone_pose.pose.position.z + z
    (x, y) = (x*cos() - y*sin(), x*sin() + y*cos())
    set_position(x, y, z)

    rate.sleep()

    while not secure_accuracy(Drone_local, goal_pose):
        set_position (x, y, z)

        rate.sleep()

#Segue bem a ideia do set_rotation
def rel_rotation (theta):
    global goal_rotation
    #nesta conversao de graus para radianos ja e' realizada a divisao por 2 que corrige a rotacao do quaternion
    #pois a conversao correta exige uma divisao por 180 graus, neste caso estamos fazendo ja por 360 (2*180)
    theta = math.pi*theta/360
    #Este if nao e' necessario, o esses fatores serao constantes, sendo o z sempre 1 e o resto 0, para que o drone gira apenas entorno de Z
#    if x*x + y*y + z*z != 1:
#        norm = math.sqrt((x*x) + (y*yo) + (z*z))
#        x /= norm
#        y /= norm
#        z /= norm
    relative_rotation = Quaternion()
    relative_rotation.x = math.sin(theta)*x
    relative_rotation.y = math.sin(theta)*y
    relative_rotation.z = math.sin(theta)*z
    relative_rotation.w = math.cos(theta)

    result = Quaternion()
    result.w = -(relative_rotation.x*goal_rotation.x) - (relative_rotation.y*goal_rotation.y) - (relative_rotation.z*goal_rotation.z) +( relative_rotation.w*goal_rotation.w)
    result.x = relative_rotation.x*goal_rotation.w + relative_rotation.y*goal_rotation.z - relative_rotation.z*goal_rotation.y + relative_rotation.w*goal_rotation.x
    result.y = -relative_rotation.x*goal_rotation.z + relative_rotation.y*goal_rotation.w + relative_rotation.z*goal_rotation.x + relative_rotation.w*goal_rotation.y
    result.z = relative_rotation.x*goal_rotation.y - relative_rotation.y*goal_rotation.x + relative_rotation.z*goal_rotation.w + relative_rotation.w*goal_rotation.z
    goal_rotation = result


rospy.init_node('Vel_Control_Node', anonymous = True)

rate = rospy.Rate(20)

local_position_pub = rospy.Publisher('/mavros/setpoint_position/local', PoseStamped, queue_size = 100)

########### Subscribers ##################
local_atual = rospy.Subscriber('/mavros/local_position/pose', PoseStamped, local_callback)

state_status_subscribe = rospy.Subscriber('/mavros/state', State, state_callback)

############## Services ##################

arm = rospy.ServiceProxy('/mavros/cmd/arming', mavros_msgs.srv.CommandBool)

set_mode = rospy.ServiceProxy('/mavros/set_mode', mavros_msgs.srv.SetMode)

set_position(0,0,0)
for i in range(300):
    local_position_pub.publish(goal_pose)
    arm(True)
    rate.sleep()

rospy.loginfo("[ROS] SETUP CONCLUIDO")
