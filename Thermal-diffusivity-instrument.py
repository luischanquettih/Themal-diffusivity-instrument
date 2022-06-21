import pyvisa
import math
from time import sleep
import time
rm = pyvisa.ResourceManager()
rm.list_resources()
inst = rm.open_resource('ASRL/dev/ttyACM0::INSTR')
inst.write_termination = "\n"
inst.read_termination = "\n"
#print(inst.query("*IDN?"))
# print(inst.query("SYSTem:THD:TEMPerature1?"))
# time.sleep(1)
# print(inst.query("SYSTem:THD:TEMPerature2?"))
# time.sleep(1)
pi = 3.14159265358979323
f = 100 #frecuencia Hz
t = 0.0
while True:
    try:
        y = int(127.5*(math.sin(2*pi*f*t)+1))
        print(t,y)
        t += 1/(100*f)
        time.sleep(0.1)
        inst.write("SYSTem:THD:VOLTage {}".format(y))
    except KeyboardInterrupt: #por si ocurre error
        break
