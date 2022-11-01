import machine
import time

analog_value = machine.ADC(26)

def read_adc():
    """"""
    return analog_value.read_u16() / 65535 * 3.3