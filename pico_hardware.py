import machine
import utime

class adc:
    """
    Access ADC of Raspi Pico
    :param: channel: 0, 1 or 2 (check PICO pinout)
    """

    vref = 3.3

    def __init__(self, channel):
        if channel == 0:
            self.analog_value = machine.ADC(31)
        elif channel == 1:
            self.analog_value = machine.ADC(32)
        elif channel == 2:
            self.analog_value = machine.ADC(34)
        else:
            raise Exception("ADC channel must be either 0, 1 or 2 (see Rasp PICO pinout)")

        self.channel = channel

    def read(self):
        return self.analog_value.read_u16() / 65535 * self.vref


class led:
    """
    Monitor any LED with Raspi Pico
    """
    def __init__(self, pin="board", start_state=0):
        if pin == "board":
            self.pin = 25
        else:
            self.pin = pin

        self.start_state = start_state
        self.led = machine.Pin(self.pin, machine.Pin.OUT, value=self.start_state)

    def toggle(self):
        self.led.toggle()

    def on(self):
        self.led.on()

    def off(self):
        self.led.off()


class mux:
    """
    Multiplexer switcher
    """
    none = 16

    def __init__(self, s0_Pin, s1_Pin, s2_Pin, s3_Pin, e_Pin):
        self.s0_Pin = s0_Pin
        self.s1_Pin = s1_Pin
        self.s2_Pin = s2_Pin
        self.s3_Pin = s3_Pin
        self.e_Pin = e_Pin

        self.s0 = machine.Pin(self.s0_Pin, machine.Pin.OUT)
        self.s1 = machine.Pin(self.s1_Pin, machine.Pin.OUT)
        self.s2 = machine.Pin(self.s2_Pin, machine.Pin.OUT)
        self.s3 = machine.Pin(self.s3_Pin, machine.Pin.OUT)
        self.e = machine.Pin(self.e_Pin, machine.Pin.OUT)

    def set(self, channel):
        if channel is not None:
            logic = channel.tobytes()
            self.s0.value((logic & 1))  # bitwise AND operation
            self.s1.value((logic & 2) >> 1)  # bitwise AND operation + shift to return either 0 or 1
            self.s2.value((logic & 4) >> 2)  # bitwise AND operation + shift to return either 0 or 1
            self.s3.value((logic & 8) >> 3)  # bitwise AND operation + shift to return either 0 or 1
            utime.sleep_us(2)  # generous time for switch to happen
        elif 0 < channel < 15:
            self.e.value(1)
        else:
            raise Exception("Channel number must be from 0 to 15 or None")


