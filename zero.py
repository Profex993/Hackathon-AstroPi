import time

from sense_hat import SenseHat

sense = SenseHat()
sense.set_rotation(270, False)

sense.color.gain = 60
sense.color.integration_cycles = 64

b = (0, 0, 0)
rgb = sense.color
c = (rgb.red, rgb.green, rgb.blue)


def anim():
    sense.set_pixels([
        b, b, b, b, b, b, b, b,
        b, b, b, c, c, b, b, b,
        b, c, b, c, c, b, c, b,
        c, c, c, c, c, c, c, c,
        b, b, c, c, c, c, b, b,
        b, b, b, c, c, b, b, b,
        b, c, b, b, b, b, c, b,
        c, b, b, b, b, b, b, c
    ])
    time.sleep(0.5)

    sense.set_pixels([
        b, b, b, c, c, b, b, b,
        b, b, c, c, c, c, b, b,
        b, c, b, c, c, b, c, b,
        b, c, c, c, c, c, c, b,
        b, b, b, c, c, b, b, b,
        b, b, b, c, c, b, b, b,
        b, b, c, b, b, c, b, b,
        b, c, b, b, b, b, c, b
    ])
    time.sleep(0.5)


for i in range(20):
    anim()
