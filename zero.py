import time
from sense_hat import SenseHat

sense = SenseHat()
sense.set_rotation(270, False)

sense.color.gain = 60
sense.color.integration_cycles = 64

# Key values
temp = sense.get_temperature()
press = sense.get_pressure()
hum = sense.get_humidity()

# Defining colors
a = (0, 0, 0)  # Black
b = (0, 128, 0)  # Green (Humidity)
c = (255, 255, 255)  # White (Default)
rgb = sense.color
d = (rgb.red, rgb.green, rgb.blue)  # Light color (Dynamic)

# Temperature color (for temp >= 90)
t = (255, 0, 0)  # Red for temperature
h = (0, 0, 139)  # Dark Blue for pressure

# Base grid (for anim)
base_grid = [
    c, c, a, a, a, a, c, c,
    c, c, a, a, a, a, c, c,
    a, a, c, c, c, c, a, a,
    c, c, a, b, b, a, c, c,
    c, c, a, b, b, a, c, c,
    a, a, a, b, b, a, a, a,
    a, b, a, b, b, a, b, a,
    a, a, b, b, b, b, a, a
]

def change_color(grid, old_color, new_color):
    """Change all instances of old_color in the grid to new_color, except for b."""
    return [new_color if pixel == old_color and pixel != b else pixel for pixel in grid]

def temp_anim():
    """Change all 'c' to 't' for temperature animation (Red for temp >= 90)."""
    grid = change_color(base_grid, c, t)
    sense.set_pixels(grid)

def pressure_anim():
    """Change all 'c' to 'a', except for 'b' (Black for pressure >= 1000)."""
    grid = change_color(base_grid, c, a)
    sense.set_pixels(grid)

def humidity_anim():
    """Change all 'c' to 'b' for humidity (Green for hum >= 50)."""
    grid = change_color(base_grid, c, h)
    sense.set_pixels(grid)

def light_anim():
    """Change all 'c' to the current light color (RGB)."""
    grid = change_color(base_grid, c, d)
    sense.set_pixels(grid)

def update_display():
    """Check and update the grid for temperature, pressure, and humidity."""
    grid = base_grid[:]
    
    if temp >= 90:  # Update temperature
        grid = change_color(grid, c, t)
    
    if press >= 1000:  # Update pressure
        grid = change_color(grid, c, a)
    
    if hum >= 50:  # Update humidity
        grid = change_color(grid, c, h)
    
    if rgb.red != 0 or rgb.green != 0 or rgb.blue != 0:  # Any light color
        grid = change_color(grid, c, d)
    
    sense.set_pixels(grid)

# Variables to track the current state of each condition
last_temp = temp
last_press = press
last_hum = hum
last_rgb = rgb  # To track the last light color

# Variables for tracking the animations
active_animations = []

# Continuous loop to check the values and react accordingly
while True:
    # Get sensor values
    temp = sense.get_temperature()
    press = sense.get_pressure()
    hum = sense.get_humidity()
    rgb = sense.color

    # Check if any condition has changed
    if temp != last_temp or press != last_press or hum != last_hum or rgb != last_rgb:
        # Update last known values
        last_temp = temp
        last_press = press
        last_hum = hum
        last_rgb = rgb
        
        # Determine which animations should be active
        active_animations = []
        if temp >= 90:
            active_animations.append(temp_anim)
        if press >= 1000:
            active_animations.append(pressure_anim)
        if hum >= 50:
            active_animations.append(humidity_anim)
        if rgb.red != 0 or rgb.green != 0 or rgb.blue != 0:
            active_animations.append(light_anim)

    # If any active animations exist, alternate between them
    if active_animations:
        for anim in active_animations:
            anim()
            time.sleep(0.3)  # Brief pause before switching to next animation

    else:
        # Default animation if no conditions are met
        update_display()
    
    # Small delay before checking again to avoid overloading the processor
    time.sleep(0.3)

