import math
import numpy as np
import matplotlib.pyplot as plt
import pickle


class trajectory():

    def __init__(self,heading,angle_of_attack,lat,long,alt) -> None:

        self.heading = heading # deg
        self.angle_of_attack = angle_of_attack  # 30 degrees pitch for descent
        self.start_lat = lat # deg
        self.start_long = long # deg
        self.start_alt = alt # meter

        self.path = []
        self.real_path = []

        self.generate_path()
        self.save_path()

    def calculate_next_gps(self,current_lat, current_long, current_alt, heading, angle_of_attack, step_distance):
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

    def generate_path(self):

        distance_to_crush = self.start_alt/math.sin(math.radians(self.angle_of_attack))
        
        step_distance = 0.01 # meter
        start = 0 
        stop = distance_to_crush - 3 # stop before crush

        current_lat = self.start_lat
        current_alt = self.start_alt
        current_long = self.start_long

        for i in np.arange(start, stop, step_distance):
            new_record = self.calculate_next_gps(current_lat, current_long, current_alt, self.heading, self.angle_of_attack, step_distance)
            self.path.append(new_record)
            current_lat, current_long, current_alt = new_record
            # print(f"Next GPS Coordinates predicted: Lat={current_lat}, Long={current_long}, Alt={current_alt}")

    def real_path_step(self,lat,long,alt):
        point = (lat,long,alt)
        self.real_path.append(point)

    def print_path(self):
        for point in self.path:
            lat, long, alt = point
            print(f"Next GPS Coordinates predicted: Lat={lat}, Long={long}, Alt={alt}")


    def plot_path(self):

        # Extracting latitude, longitude, and altitude from the trajectory
        latitudes, longitudes, altitudes = zip(*self.path)

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

    
    def save_path(self):
        with open(f'/ardupilot/Tools/cocpit_environment/with_pymavlink/saved_data/predicted_gps_path/path_{self.angle_of_attack}.pkl', 'wb') as file:
            pickle.dump(self.path, file)
        self.progress(f"save path_{self.angle_of_attack}.pkl")
        
    def save_real_path(self):
        with open(f'/ardupilot/Tools/cocpit_environment/with_pymavlink/saved_data/predicted_gps_path/real_path_{self.angle_of_attack}.pkl', 'wb') as file:
            pickle.dump(self.real_path, file)
        self.progress(f"save real_path_{self.angle_of_attack}.pkl")


    def progress(self,data):
        print(f"PATH: {data}")



# # Example usage
# heading = 47.98
# angle_of_attack = 80  # 30 degrees pitch for descent
# start_lat = -35.3575561 # deg
# start_long = 149.1725349 # deg
# start_alt = 100 # meter

# def calculate_next_gps(current_lat, current_long, current_alt, heading, angle_of_attack, step_distance):
#     # Earth radius in kilometers
#     R = 6371.0

#     # Convert heading to radians
#     heading_rad = math.radians(heading)
    
#     # Convert angle of attack to radians
#     angle_of_attack_rad = math.radians(angle_of_attack)

#     # Calculate the change in latitude and longitude
#     delta_lat = (step_distance * math.cos(heading_rad) * math.cos(angle_of_attack_rad)) / R
#     delta_long = (step_distance * math.sin(heading_rad) * math.cos(angle_of_attack_rad)) / (R * math.cos(math.radians(current_lat)))

#     # Calculate new latitude and longitude
#     new_lat = current_lat + math.degrees(delta_lat)
#     new_long = current_long + math.degrees(delta_long)

#     # Assuming a linear descent, update altitude
#     new_alt = current_alt - step_distance * math.sin(angle_of_attack_rad)

#     return new_lat, new_long, new_alt




# def generate_trajectory(start_lat, start_long, start_alt, heading, angle_of_attack):

#     trajectory = []

#     distance_to_crush = start_alt/math.sin(math.radians(angle_of_attack))
    
#     step_distance = 0.01 # meter
#     start = 0 
#     stop = distance_to_crush  # -10 ,stop before crush

#     current_lat = start_lat
#     current_alt = start_alt
#     current_long = start_long

#     for i in np.arange(start, stop, step_distance):
#         new_lat, new_long, new_alt = calculate_next_gps(current_lat, current_long, current_alt, heading, angle_of_attack, step_distance)
#         trajectory.append((new_lat,new_long,new_alt))
#         print(f"Next GPS Coordinates: Lat={new_lat}, Long={new_long}, Alt={new_alt}")
#         current_alt = new_alt
#         current_lat = new_lat
#         current_long = new_long

# def plot_trajectory():

#     # Extracting latitude, longitude, and altitude from the trajectory
#     latitudes, longitudes, altitudes = zip(*trajectory)

#     # Creating a 3D plot
#     fig = plt.figure()
#     ax = fig.add_subplot(111, projection='3d')

#     # Plotting the trajectory
#     ax.plot3D(longitudes, latitudes, altitudes, marker='o')

#     # Adding labels
#     ax.set_xlabel('Longitude')
#     ax.set_ylabel('Latitude')
#     ax.set_zlabel('Altitude')

#     # Show the plot
#     plt.show()



# generate_trajectory(start_lat,start_long,start_alt,heading,angle_of_attack)