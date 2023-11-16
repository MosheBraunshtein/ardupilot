import math

def calculate_distance(point1, point2):
    return math.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)

def calculate_line_equation(point1, point2):
    # Calculate the slope (m) and y-intercept (b) of the line
    m = (point2[1] - point1[1]) / (point2[0] - point1[0])
    b = point1[1] - m * point1[0]

    return m, b

def distance_from_line(point, line_equation):
    # Extract slope (m) and y-intercept (b) from the line equation
    m, b = line_equation

    # Calculate the y-coordinate on the line corresponding to the x-coordinate of the point
    y_on_line = m * point[0] + b

    # Calculate the distance between the point and the point on the line
    distance = calculate_distance(point, (point[0], y_on_line))

    return distance

# Example usage
point1 = (1, 2)
point2 = (4, 5)
point_to_measure = (10, 3)

# Calculate line equation
line_equation = calculate_line_equation(point1, point2)

# Calculate distance from the point to the line
distance = distance_from_line(point_to_measure, line_equation)

print(f"The distance from {point_to_measure} to the line passing through {point1} and {point2} is {distance:.2f} units.")
