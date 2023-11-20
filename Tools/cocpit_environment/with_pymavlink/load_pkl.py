import pickle
import matplotlib.pyplot as plt
import argparse



parser = argparse.ArgumentParser()
parser.add_argument("-angle",help="specify angle for trajectory")
args = parser.parse_args()

# Creating a 3D plot
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')


# Load real path from the file
with open(f'saved_data/predicted_gps_path/real_path_{args.angle}.pkl', 'rb') as file:
    real_path = pickle.load(file)

real_latitudes, real_longitudes, real_altitudes = zip(*real_path)

# Plotting the trajectory
ax.plot3D(real_longitudes, real_latitudes, real_altitudes, label='Real Path', linestyle='-', color='blue', alpha=0.7)


# Load ref path from the file
with open(f'saved_data/predicted_gps_path/path_{args.angle}.pkl', 'rb') as file:
    ref_path = pickle.load(file)

ref_latitudes, ref_longitudes, ref_altitudes = zip(*ref_path)

# Plotting the trajectory
ax.plot3D(ref_longitudes, ref_latitudes, ref_altitudes, label='Reference Path', linestyle='-', color='red', alpha=0.7)




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
plt.title(f'Trajectory Plot - Angle {args.angle}')

plt.show()