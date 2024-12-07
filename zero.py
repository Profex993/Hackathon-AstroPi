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
a = (0, 0, 0)  # Black (Pressure)
b = (0, 128, 0)  # Green (grass)
c = (255, 255, 255)  # White (Default)

# Temperature colors
t = (255, 0, 0)  # Red for temp >= 50
t_minus = (135, 206, 235)  # Light Blue for temp <= 0

# Humidity colors
h = (0, 0, 255)  # Blue for humidity >= 80%
h_minus = (255, 165, 0)  # Orange for humidity <= 40%

# Base grid (for anim)
base_grid = [
    c, c, a, c, c, a, c, c,
    c, c, a, a, a, a, c, c,
    a, a, c, c, c, c, a, a,
    c, c, a, b, b, a, c, c,
    c, c, a, b, b, a, c, c,
    a, a, a, b, b, a, a, a,
    a, b, a, b, b, a, b, a,
    a, a, b, b, b, b, a, a
]

# Function to change colors in the grid
def change_color(grid, old_color, new_color):
    """Change all instances of old_color in the grid to new_color, except for b."""
    return [new_color if pixel == old_color and pixel != b else pixel for pixel in grid]

# Animation functions
def temp_anim():
    """Change all 'c' to 't' for temperature animation (Red for temp >= 50)."""
    grid = change_color(base_grid, c, t)
    sense.set_pixels(grid)

def temp_minus_anim():
    """Change all 'c' to 't_minus' for temperature below 0 animation (Light Blue for temp <= 0)."""
    grid = change_color(base_grid, c, t_minus)
    sense.set_pixels(grid)

def pressure_anim():
    """Change all 'c' to 'a', except for 'b' (Black for pressure >= 1000)."""
    grid = change_color(base_grid, c, a)
    sense.set_pixels(grid)

def humidity_anim():
    """Change all 'c' to 'h' for high humidity (Blue for hum >= 80%)."""
    grid = change_color(base_grid, c, h)
    sense.set_pixels(grid)

def humidity_minus_anim():
    """Change all 'c' to 'h_minus' for low humidity (Orange for hum <= 40%)."""
    grid = change_color(base_grid, c, h_minus)
    sense.set_pixels(grid)

def light_anim(light_color):
    """Change all 'c' to the dynamic light color."""
    grid = change_color(base_grid, c, light_color)
    sense.set_pixels(grid)

# Update display based on conditions
def update_display():
    """Check and update the grid for temperature, pressure, humidity, and light color."""
    grid = base_grid[:]

    if temp >= 50:  # Update temperature for high temp
        grid = change_color(grid, c, t)
    
    if temp <= 0:  # Update temperature for low temp
        grid = change_color(grid, c, t_minus)
    
    if press >= 1000:  # Update pressure
        grid = change_color(grid, c, a)
    
    if hum >= 80:  # Update humidity for high humidity
        grid = change_color(grid, c, h)
    
    if hum <= 40:  # Update humidity for low humidity
        grid = change_color(grid, c, h_minus)
    
    # Update light dynamically
    rgb = sense.color
    light_color = (rgb.red, rgb.green, rgb.blue)
    grid = change_color(grid, c, light_color)
    
    sense.set_pixels(grid)

# Continuous loop to check the values and react accordingly
while True:
    # Get sensor values
    temp = sense.get_temperature()
    press = sense.get_pressure()
    hum = sense.get_humidity()
    rgb = sense.color  # Dynamic light sensor

    # Determine the active animations based on conditions
    active_animations = []

    # Temperature check
    if temp >= 50:
        active_animations.append(temp_anim)
    elif temp <= 0:
        active_animations.append(temp_minus_anim)

    # Pressure check
    if press >= 1000:
        active_animations.append(pressure_anim)

    # Humidity check
    if hum >= 80:
        active_animations.append(humidity_anim)
    elif hum <= 40:
        active_animations.append(humidity_minus_anim)

    # Light check
    if rgb.red != 0 or rgb.green != 0 or rgb.blue != 0:  # Any detected light
        active_animations.append(lambda: light_anim((rgb.red, rgb.green, rgb.blue)))

    # Update the display with the active animations
    if active_animations:
        for anim in active_animations:
            anim()  # Execute the current animation
            time.sleep(0.3)  # Switch animations every 0.3 seconds

    else:
        # Default animation if no conditions are met
        update_display()
    
    # Small delay before checking again to avoid overloading the processor
    time.sleep(0.3)  # Delay for checking changes

