from machine import ADC
from utime import ticks_add, ticks_ms, ticks_diff, sleep
from math import sqrt

ct_2 = ADC(26)

averaged = 10
ct_ratio = 5

class ct:
    adc = ADC(26)
    reading = []

    def __init__(self, ct_ratio, samples_averaged=10):
        self.ratio = ct_ratio
        self.timeout = 20
        self.samples_averaged = samples_averaged

    def read(self):
        timeout = ticks_add(ticks_ms(), 20)  # max ticks is 1073741823
        reading = []
        while ticks_diff(timeout, ticks_ms()) > 0:
            raw = 0
            for _ in range(self.samples_averaged):
                raw += round(self.adc.read_u16(), 3)
            raw = ((raw / 65536 * 3.3 / self.samples_averaged) - (3.3 / 2))
            reading.append(raw)
        return reading


    def current_rms(self):
        reading = ct.read(self)
        self.rms = round(sqrt(sum([x ** 2 for x in reading]) / len(reading)) * ct_ratio, 3)
        if self.rms <= 0.032:
            self.rms = 0
        return self.rms


radiateur = ct(5)
while True:
    print(radiateur.current_rms())
    sleep(0.25)


