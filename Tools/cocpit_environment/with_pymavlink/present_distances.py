import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math 

# Assuming `points` is a list of tuples where each tuple represents a point (lat, long, alt)
path = [(0, 0, 0), (1, 1, 1), (2, 2, 2), (3, 3, 3)]

point_A = (0.5,1.5,2)

# Extract coordinates
latitudes, longitudes, altitudes = zip(*path)

# Plot 3D line
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(latitudes, longitudes, altitudes, marker='o')

lat,long,alt = point_A
ax.scatter(lat,long,alt,marker='3',color='red',s=500)


ax.set_xlabel('Latitude')
ax.set_ylabel('Longitude')
ax.set_zlabel('Altitude')

# Calculate distance and plot lines
for i, (x, y, z) in enumerate(path):
    distance = math.sqrt((lat - x)**2 + (long - y)**2 + (alt - z)**2)
    
    # Plot line connecting point_A to each point on the path
    ax.plot([lat, x], [long, y], [alt, z], linestyle='dashed', color='gray', alpha=0.5)

    # Annotate distance near the line
    ax.text((lat + x) / 2, (long + y) / 2, (alt + z) / 2, f'{distance:.2f}', color='red')

# min_distance = min(distances)
# print(f"Minimum distance between point_A and the path: {min_distance:.2f} units")

plt.show()