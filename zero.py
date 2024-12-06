import time

from sense_hat import SenseHat

sense = SenseHat()
sense.set_rotation(270, False)

sense.color.gain = 60
sense.color.integration_cycles = 64

a = (0, 0, 0)
b = (0, 128, 0)
c = (255, 255, 255)
rgb = sense.color
d = (rgb.red, rgb.green, rgb.blue)


def anim():
    sense.set_pixels([ #Default state. :)
        c, c, a, a, a, a, c, c,
        c, c, a, a, a, a, c, c,
        a, a, c, c, c, c, a, a,
        c, c, a, b, b, a, c, c,
        c, c, a, b, b, a, c, c,
        a, a, a, b, b, a, a, a,
        a, b, a, b, b, a, b, a,
        a, a, b, b, b, b, a, a
    ])
    time.sleep(0.5)

    sense.set_pixels([
        d, d, a, a, a, a, d, d,
        d, d, a, a, a, a, d, d,
        a, a, d, d, d, d, a, a,
        d, d, a, b, b, a, d, d,
        d, d, a, b, b, a, d, d,
        a, a, a, b, b, a, a, a,
        a, b, a, b, b, a, b, a,
        a, a, b, b, b, b, a, a
    ])
    time.sleep(0.5)


for i in range(20):
    anim()
