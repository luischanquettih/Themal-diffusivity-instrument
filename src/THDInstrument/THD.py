import threading
import time
import math
import numpy as numpy
from time import sleep
from firebase import firebase
import funciones
import pyvisa
rm = pyvisa.ResourceManager()
rm.list_resources()

import hardware
THD = hardware.THD_Arduino()

def infiniteloop1():
    from firebase import firebase
    firebase = firebase.FirebaseApplication('https://fc-remotelaboratory-default-rtdb.firebaseio.com', None)
    A = 5
    t0 = time.time()
   
    while True:
        f = 0.0083
       
        t = time.time()-t0
        y = A*numpy.sin(2*numpy.pi*f*t) + A
        THD.set_voltage(y)
        print(t,pwm)
        print(f)

def infiniteloop2():
    from firebase import firebase
    firebase = firebase.FirebaseApplication('https://fc-remotelaboratory-default-rtdb.firebaseio.com', None)
    i=1
    while True:
        temp1 = THD.Temperature1
        temp2 = THD.Temperature2
        firebase.patch('/Measure/Temperature1/',{str(i): float(temp1)})
        firebase.patch('/Measure/Temperature2/',{str(i): float(temp2)})
        i += 1
        time.sleep(1)

thread1 = threading.Thread(target=infiniteloop1)
thread1.start()
thread2 = threading.Thread(target=infiniteloop2)
thread2.start()
