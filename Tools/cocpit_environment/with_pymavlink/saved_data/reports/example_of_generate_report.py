import sys


# Save the output to a text file
filename = "output.txt"
with open(filename, "w") as file:
    sys.stdout = file  # Redirect standard output to the file

    print("report 2")

    sys.stdout = sys.__stdout__  # Reset standard output to the console

print(f"Output saved to {filename}")
