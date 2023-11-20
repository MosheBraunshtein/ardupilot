import pickle

# Sample list of tuples
data = [(1, 2, 3), (3, 4, 3), (5, 6, 3)]

# Save to a file
with open('saved_data/predicted_gps_path/data1.pkl', 'wb') as file:
    pickle.dump(data, file)