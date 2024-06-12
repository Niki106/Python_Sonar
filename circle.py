import numpy as np

from matplotlib.patches import Circle
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt

center = (0.5, 0.5)
radius = 0.4

circle = Circle(xy=center, radius=radius, fill=False)

fig, ax = plt.subplots()

# ax.add_patch(circle)
ax.set_aspect("equal")

# Function to calculate startpoint coordinates for a given angle
def get_startpoint_xy(theta):
  x_startpoint = center[0] + radius * np.cos(np.radians(theta))
  y_startpoint = center[1] + radius * np.sin(np.radians(theta))
  return x_startpoint, y_startpoint

# Function to calculate endpoint coordinates for a given angle
def get_endpoint_xy(theta, extension):
  x, y = get_startpoint_xy(theta)
  x_endpoint = x + extension * np.cos(np.radians(theta))
  y_endpoint = y + extension * np.sin(np.radians(theta))
  return x_endpoint, y_endpoint

def draw_line(theta, extension, color):
  x1, y1 = get_startpoint_xy(theta)
  x2, y2 = get_endpoint_xy(theta, extension)
  plt.plot([x1, x2], [y1, y2], color=color)


num_angles = 72  # Adjust for number of lines (360 / 10)
step_size = 5  # Degrees between lines

for i in range(num_angles):
  theta = i * step_size
  if theta < 30: extension = 0.2; color = 'red'
  elif theta < 60: extension = 0.5; color = 'blue'
  elif theta < 90: extension = 0.3; color = 'green'
  elif theta < 120: extension = 0.1; color = 'red'
  elif theta < 150: extension = 0.3; color = 'blue'
  elif theta < 180: extension = 0.2; color = 'green'
  elif theta < 210: extension = 0.5; color = 'yellow'
  elif theta < 240: extension = 0.5; color = 'green'

  draw_line(theta, extension, color)
  

plt.xlim([-2.3 * radius + center[0], 2.3 * radius + center[0]])
plt.ylim([-2.3 * radius + center[1], 2.3 * radius + center[1]])
ax.axis('off')

plt.savefig("my_plot.pdf", format="pdf", bbox_inches="tight")

plt.show()