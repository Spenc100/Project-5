#Spencer Schmid
#MPP193 
#Project 5

#Worked with Akshita Rao

from time import sleep
from rp2 import PIO
from rp2 import StateMachine
from rp2 import asm_pio
from machine import Pin

max_counting=1000
min_out=100
@asm_pio(sideset_init=PIO.OUT_LOW)


def pwm_prog():
    # fmt: off
    pull(noblock).side(0)
    mov(x, osr) 
    mov(y, isr) 
    
    #start pwm loop
    jmp(x_not_y,"skip")
    label("pwmloop")
    nop().side(1)
    label("skip")
    jmp(y_dec,"pwmloop")
    # fmt: on

class PIOPWM:
    def __init__(self, sm_id, pin, max_count, count_freq):
        self._sm = StateMachine(sm_id, pwm_prog, freq=freq, sideset_base=Pin(pin))

        self._sm.put(max_count)
        self._sm.exec("pull()")
        self._sm.exec("mov(isr, osr)")
        self._sm.active(1)
        self._max_count = max_count

    def set(self, value):
        value = max(value,-1)
        value = min(value, self._max_count)
        self._sm.put(value)

#Setting motor to be in Pin 15 and initializing state machine
mtr_sm= StateMachine(0, pwm_prog, freq=10000000, sideset_base=Pin(15))
mtr_sm.put(max_counting)

mtr_sm.exec("pull()")
mtr_sm.exec("mov(isr, osr)")
mtr_sm.active(1)

#Smooth motor motion
for t in range(max_counting-min_out):
    mtr_sm.put(t+min_out)
    sleep(0.001)
sleep(2.5)
for t in range(max_counting):
    mtr_sm.put(max_counting-t)
    sleep(0.001)
mtr_sm.put(0)

#Jerky motor motion
mtr_sm.put(0)
sleep(0.5)
mtr_sm.put(max_counting)
sleep(2.5)
mtr_sm.put(0)
