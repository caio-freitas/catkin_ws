#!/bin/bash

echo "[ INFO ] Opening the claw"

i=0

while [ $i -le 10 ]
do
    python3 PWM_JetsonGPIO.py
    
    i=$(( $i + 1))

    sleep 0.1

done

