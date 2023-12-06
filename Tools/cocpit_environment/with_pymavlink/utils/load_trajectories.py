import pickle
import matplotlib.pyplot as plt
import argparse
import os


parser = argparse.ArgumentParser()
parser.add_argument("-ep",help="specify angle for trajectory")
args = parser.parse_args()

# Creating a 3D plot
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

utils_path = os.path.dirname(__file__)
with_pymavlink = os.path.dirname(utils_path)

# Load real path from the file

file_realPath = os.path.join(with_pymavlink,'saved_data\\real_path\\path_40deg.pkl')
with open(file_realPath, 'rb') as file:
    real_path = pickle.load(file)

real_latitudes, real_longitudes, real_altitudes = zip(*real_path)
# Plotting the trajectory
ax.plot3D(real_longitudes, real_latitudes, real_altitudes, label='Real Path', linestyle='dotted', color='blue', alpha=0.7)
# Add start and endpoint markers for real path
ax.scatter3D(real_longitudes[0], real_latitudes[0], real_altitudes[0], marker='o', color='green', label='Real Path Start')
ax.scatter3D(real_longitudes[-1], real_latitudes[-1], real_altitudes[-1], marker='x', color='green', label='Real Path End')

# Add text annotations for real path coordinates
ax.text(real_longitudes[0], real_latitudes[0], real_altitudes[0], f'({real_longitudes[0]:.2f}, {real_latitudes[0]:.2f}, {real_altitudes[0]:.2f})', color='green')
ax.text(real_longitudes[-1], real_latitudes[-1], real_altitudes[-1], f'({real_longitudes[-1]:.2f}, {real_latitudes[-1]:.2f}, {real_altitudes[-1]:.2f})', color='green')


# Load ref path from the file

file_refPath = os.path.join(with_pymavlink,'saved_data\\ref_path\\path_40deg.pkl')
with open(file_refPath, 'rb') as file:
    ref_path = pickle.load(file)

ref_latitudes, ref_longitudes, ref_altitudes = zip(*ref_path)
ax.plot3D(ref_longitudes, ref_latitudes, ref_altitudes, label='Reference Path', linestyle='dotted', color='red', alpha=0.7)

# Add start and endpoint markers for reference path
ax.scatter3D(ref_longitudes[0], ref_latitudes[0], ref_altitudes[0], marker='o', color='orange', label='Ref Path Start')
ax.scatter3D(ref_longitudes[-1], ref_latitudes[-1], ref_altitudes[-1], marker='x', color='orange', label='Ref Path End')

# Add text annotations for reference path coordinates
ax.text(ref_longitudes[0], ref_latitudes[0], ref_altitudes[0], f'({ref_longitudes[0]:.2f}, {ref_latitudes[0]:.2f}, {ref_altitudes[0]:.2f})', color='orange')
ax.text(ref_longitudes[-1], ref_latitudes[-1], ref_altitudes[-1], f'({ref_longitudes[-1]:.2f}, {ref_latitudes[-1]:.2f}, {ref_altitudes[-1]:.2f})', color='orange')

# Adding labels
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.set_zlabel('Altitude')

# Add legends
ax.legend()

# Add grid
ax.grid(True)

# Set specific limits for better visualization
ax.set_xlim([min(min(real_longitudes), min(ref_longitudes)), max(max(real_longitudes), max(ref_longitudes))])
ax.set_ylim([min(min(real_latitudes), min(ref_latitudes)), max(max(real_latitudes), max(ref_latitudes))])
ax.set_zlim([min(min(real_altitudes), min(ref_altitudes)), max(max(real_altitudes), max(ref_altitudes))])

# Add a title
plt.title(f'Trajectory Plot - Angle 40')

plt.show()