#!/usr/bin/env python

#CODIGO COPIADO E ADAPTADO DO CODIGO "simple_pwm.py"
#na past /opt/nvidia/jetson                       -gpio/samples
#leia o readme na pasta jetson-gpio e' util
#pode haver erro de escrita no nome de alguma pasta

#BIBLIOTECA BASEADA NA RPi.GPIO qualquer informacao procurar por rpi
#se tentar usar a Jetson.gpio nas buscas na vai achar facil

import time
import Jetson.GPIO as GPIO

#pino da nano que funciona o pwm
PWM1 = 33;

def open_claw():

	#setup da placa (numeracao dos pinos pela placa)
	GPIO.setmode(GPIO.BOARD)
	#setando o pino como out com inicial alto
	GPIO.setup(PWM1, GPIO.OUT,  initial = GPIO.HIGH)
	#criando um obbjeto de pwm com parametros (pino, freq)
	p = GPIO.PWM(PWM1, 50) #USANDO 50Hz por especificacao do mot
		
	p.start(100) #iniciando o pwm com o dutycicle de parametro

	#time.sleep(0.1)
	#limpar gipos para que eles voltem para config original
	p.stop()
	GPIO.cleanup()


if __name__ == '__main__':
	open_claw()

