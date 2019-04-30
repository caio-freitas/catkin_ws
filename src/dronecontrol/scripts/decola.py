import rospy
from geometry_msgs.msg import PoseStamped
import mavros_msgs
from mavros_msgs import srv
from mavros_msgs.msg import State

posicao_atual = PoseStamped()
armado = False

def posicao_callback (data):
    global posicao_atual
    posicao_atual = data

def armado_callback(state):
    global armado
    armado = state.armed
# Inicar o node
rospy.init_node('primeiro_voo')
# iniciar o "tempo ros" (rate)
rate = rospy.Rate(20)

# Inicializar os publishers e subscribers
posicaopub = rospy.Publisher('/mavros/setpoint_position/pose',PoseStamped, queue_size=10)
posicaosub = rospy.Subscriber('/mavros/local_position/pose',PoseStamped, posicao_callback)
statesub = rospy.Subscriber('/mavros/state', State, armado_callback)
# Armar o drone
arm = rospy.ServiceProxy('/mavros/cmd/arming', mavros_msgs.srv.CommandBool)
for i in range(300):
    rate.sleep()

while not armado:
    arm(True)
    rate.sleep()
    print('armando')
# Criar uma variavel pra essa posicao
pose = PoseStamped()
#pose.pose.position.x=
pose.pose.position.x = 0
pose.pose.position.y = 0
pose.pose.position.z = 5
while not rospy.is_shutdown():
    posicaopub.publish(pose)
# Publicar uma posicao com uma altura
# Exemplo de publisher
#local_position_pub = rospy.Publisher('mavros/setpoint_position/local', PoseStamped, queue_size=10)
# Exemplo de subscriber
#state_status_subscribe = rospy.Subscriber('/mavros/state', State, state_callback)

#while not rospy.is_shutdown():
