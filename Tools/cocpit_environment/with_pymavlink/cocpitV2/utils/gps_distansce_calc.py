import math


def compute_next_ref_gps(last_ref_pose, angle_of_attack=40, step_distance=0.01) -> list:
        # Earth radius in kilometers
        R = 6371.0

        # Convert heading to radians
        heading_rad = math.radians(last_ref_pose.heading)
        
        # Convert angle of attack to radians
        angle_of_attack_rad = math.radians(angle_of_attack)

        # Calculate the change in latitude and longitude
        delta_lat = (step_distance * math.cos(heading_rad) * math.cos(angle_of_attack_rad)) / R
        delta_long = (step_distance * math.sin(heading_rad) * math.cos(angle_of_attack_rad)) / (R * math.cos(math.radians(current_lat)))

        # Calculate new latitude and longitude
        new_lat = last_ref_pose.lat + math.degrees(delta_lat)
        new_long = last_ref_pose.long + math.degrees(delta_long)

        # Assuming a linear descent, update altitude

        new_alt = last_ref_pose.alt - step_distance * math.sin(angle_of_attack_rad)

        return [new_lat, new_long, new_alt]
