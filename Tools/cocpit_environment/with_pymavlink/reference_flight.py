import math
import numpy as np
import matplotlib.pyplot as plt
import pickle


class trajectory():

    def __init__(self,heading,angle_of_attack,lat,long,alt,real_path_Nsteps) -> None:

        self.heading = heading # deg
        self.angle_of_attack = angle_of_attack  # 30 degrees pitch for descent
        self.start_lat = lat # deg
        self.start_long = long # deg
        self.start_alt = alt # meter

        self.path = []
        self.real_path = np.zeros((real_path_Nsteps,3))
        self.real_path_i = 0
        self.minimum_distance_index_prev = 0

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
        stop = round(distance_to_crush - 3) # stop before crush

        # path_Nsteps = (start - stop) / step_distance

        current_lat = self.start_lat
        current_alt = self.start_alt
        current_long = self.start_long

        for i in np.arange(start, stop, step_distance):
            new_record = self.calculate_next_gps(current_lat, current_long, current_alt, self.heading, self.angle_of_attack, step_distance)
            self.path.append(new_record)
            current_lat, current_long, current_alt = new_record
            # print(f"Next GPS Coordinates predicted: Lat={current_lat}, Long={current_long}, Alt={current_alt}")
        points = len(self.path)
        self.progress(f"calculate distance from {points} points in ref_path")

    def path_linear3d(self):
        # Assuming self.path is a list of tuples (lat, long, alt)
        path_array = np.array(self.path)

        # Create a matrix with the latitude, longitude, and a column of 1s (for the intercept term)
        X = np.column_stack((path_array[:, 0], path_array[:, 1], np.ones_like(path_array[:, 0])))

        # Altitudes are the target values
        y = path_array[:, 2]

        # Perform linear regression to find the coefficients
        coefficients, residuals, _, _ = np.linalg.lstsq(X, y, rcond=None)

        # Coefficients[0] is the slope for latitude, coefficients[1] is the slope for longitude, and coefficients[2] is the intercept
        slope_lat = coefficients[0]
        slope_long = coefficients[1]
        intercept = coefficients[2]

        # The line equation is z = ax + by + c, where a is the slope for latitude, b is the slope for longitude, and c is the intercept
        line_equation = f"z = {slope_lat:.6f}x + {slope_long:.6f}y + {intercept:.6f}"

        print("3D Line Equation:", line_equation)

    #TODO: instead of the following method: generate line from points with least squere, then calculate distance point from path
    def distance_realLocation_toPath(self,realGPS):
        points = len(self.path)
        
        
        distances = np.zeros(points)
        lat,long,alt = realGPS

        #TODO: should be more efficient
        for i, (x, y, z) in enumerate(self.path):
            distance = math.sqrt((lat - x)**2 + (long - y)**2 + (alt - z)**2)
            distances[i] = distance
            # # Plot line connecting point_A to each point on the path
            # ax.plot([lat, x], [long, y], [alt, z], linestyle='dashed', color='gray', alpha=0.5)

            # # Annotate distance near the line
            # ax.text((lat + x) / 2, (long + y) / 2, (alt + z) / 2, f'{distance:.2f}', color='red')
        # Find the index of the minimum distance
        min_distance = min(distances)
        min_distance_index = np.argmin(distances)

        bad_step = min_distance_index < self.minimum_distance_index_prev
    
        return min_distance, bad_step

    
    def real_path_step(self,lat,long,alt):

        point = (lat,long,alt)
        self.real_path[self.real_path_i] = point
        self.real_path_i += 1

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
        with open(f'/ardupilot/Tools/cocpit_environment/with_pymavlink/saved_data/real_path/real_path_{self.angle_of_attack}.pkl', 'wb') as file:
            pickle.dump(self.real_path, file)
        self.progress(f"save real_path_{self.angle_of_attack}.pkl")


    def progress(self,data):
        print(f"PATH: {data}\n")