#!/usr/bin/env python3

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Generate some example data
t = [i for i in range(10)]
x = [2*i for i in t]
y = [i**2 for i in t]
z = [0.5*i for i in t]

# Create a 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot the trajectory
ax.plot(x, y, z, label='3D Trajectory')

# Add labels
ax.set_xlabel('X Axis')
ax.set_ylabel('Y Axis')
ax.set_zlabel('Z Axis')

# Add a legend
ax.legend()

# Show the plot
plt.show()
