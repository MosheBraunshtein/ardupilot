import math
import numpy as np
import matplotlib.pyplot as plt



# Example usage
heading = 47.98
angle_of_attack = 80  # 30 degrees pitch for descent
start_lat = -35.3575561 # deg
start_long = 149.1725349 # deg
start_alt = 100 # meter

def calculate_next_gps(current_lat, current_long, current_alt, heading, angle_of_attack, step_distance):
    # Earth radius in kilometers
    R = 6371.0

    # Convert heading to radians
    heading_rad = math.radians(heading)
    
    # Convert angle of attack to radians
    angle_of_attack_rad = math.radians(angle_of_attack)

    # Calculate the change in latitude and longitude
    delta_lat = (step_distance * math.cos(heading_rad) * math.cos(angle_of_attack_rad)) / R
    delta_long = (step_distance * math.sin(heading_rad) * math.cos(angle_of_attack_rad)) / (R * math.cos(math.radians(current_lat)))

    # Calculate new latitude and longitude
    new_lat = current_lat + math.degrees(delta_lat)
    new_long = current_long + math.degrees(delta_long)

    # Assuming a linear descent, update altitude
    new_alt = current_alt - step_distance * math.sin(angle_of_attack_rad)

    return new_lat, new_long, new_alt




def generate_trajectory(start_lat, start_long, start_alt, heading, angle_of_attack):

    trajectory = []

    distance_to_crush = start_alt/math.sin(math.radians(angle_of_attack))
    
    step_distance = 0.01 # meter
    start = 0 
    stop = distance_to_crush  # -10 ,stop before crush

    current_lat = start_lat
    current_alt = start_alt
    current_long = start_long

    for i in np.arange(start, stop, step_distance):
        new_lat, new_long, new_alt = calculate_next_gps(current_lat, current_long, current_alt, heading, angle_of_attack, step_distance)
        trajectory.append((new_lat,new_long,new_alt))
        print(f"Next GPS Coordinates: Lat={new_lat}, Long={new_long}, Alt={new_alt}")
        current_alt = new_alt
        current_lat = new_lat
        current_long = new_long

    # Extracting latitude, longitude, and altitude from the trajectory
    latitudes, longitudes, altitudes = zip(*trajectory)

    # Creating a 3D plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Plotting the trajectory
    ax.plot3D(longitudes, latitudes, altitudes, marker='o')

    # Adding labels
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_zlabel('Altitude')

    # Show the plot
    plt.show()



generate_trajectory(start_lat,start_long,start_alt,heading,angle_of_attack)