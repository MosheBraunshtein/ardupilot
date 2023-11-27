import math

# Point 1
lat1, long1, alt1 = -35.3628983,  149.1651667, 2.8799999999999955

# Point 2
lat2, long2, alt2 = -34.33939653203505, 149.0069549676634, 2.8939881928679045

##############################################################################################################################

# Convert degrees to radians
lat1, long1, lat2, long2 = map(math.radians, [lat1, long1, lat2, long2])

# Haversine formula
delta_lat = lat2 - lat1
delta_long = long2 - long1

a = math.sin(delta_lat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(delta_long / 2) ** 2
c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

# Earth's radius in kilometers
R = 6371.0

# Calculate the horizontal distance
distance_horizontal = R * c

# Calculate the total distance including altitude
distance_total_m = math.sqrt(distance_horizontal ** 2 + (alt2 - alt1) ** 2) * 1000

# print("first method")
# print(f"Distance: {distance_total_m:.2f} m")

##############################################################################################################################


def spherical_law_of_cosines(coord1, coord2):
    lat1, lon1, alt1 = coord1
    lat2, lon2, alt2 = coord2

    # Convert degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Spherical law of cosines formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    # Earth's radius in kilometers
    radius_earth = 6371

    # Include altitude difference
    distance = math.sqrt((radius_earth * c)**2 + (alt2 - alt1)**2)

    return distance

# Example usage
coord1 = (lat1, long1, alt1)  # Los Angeles, altitude 100 meters
coord2 = (lat2, long2, alt2)  # San Francisco, altitude 50 meters

distance_m = spherical_law_of_cosines(coord1, coord2) * 1000
# print("\nsecond method")
# print(f"Distance: {distance_m:.2f} m")


###############################################################################################################################


def geodetic_to_ecef(latitude, longitude, altitude):
    a = 6378137.0  # semi-major axis of the Earth
    f = 1 / 298.257223563  # flattening
    b = (1 - f) * a  # semi-minor axis of the Earth

    phi = math.radians(latitude)
    lam = math.radians(longitude)
    h = altitude

    N = a / math.sqrt(1 - f * (2 - f) * math.sin(phi)**2)

    X = (N + h) * math.cos(phi) * math.cos(lam)
    Y = (N + h) * math.cos(phi) * math.sin(lam)
    Z = ((b**2 / a**2) * N + h) * math.sin(phi)

    return X, Y, Z


X1, Y1, Z1 = geodetic_to_ecef(lat1, long1, alt1)
X2, Y2, Z2 = geodetic_to_ecef(lat2, long2, alt2)

distance = math.sqrt((X1 - X2)**2 + (Y1 - Y2)**2 + (Z1 - Z2)**2)
# print("\nthird method")
# print(f"Distance: {distance_m:.2f} ")