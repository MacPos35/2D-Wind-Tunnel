import pandas as pd
import matplotlib.pyplot as plt

# Constants
q_inf = 335.7613443  # Free-stream dynamic pressure (Pa)

# Load Excel data (sensor positions)
excel_data = pd.read_excel('DATA_ANALYSIS/PPS.xlsx', header=None)
# Extract sensor positions from Column B, Row 3 to Row 51 (adjusting for zero-indexing)
sensor_positions = excel_data.iloc[3:52, 1]  # Rows 3 to 51, Column B

# Load text file data (angles of attack and pressure values)
text_data = pd.read_csv('DATA_ANALYSIS/raw_2d.txt', sep="\t", header=None)

# Extract angles of attack (starting from Column 3, Row 3 in text file)
angles_of_attack = text_data.iloc[2:, 2]  # Extract from Row 3, Column 3 onwards

# Convert angles of attack to numeric (to avoid any string/float issues)
angles_of_attack = pd.to_numeric(angles_of_attack, errors='coerce')

# Extract pressure values (Columns 9 to 57 starting from Row 3 in text file)
pressure_values = text_data.iloc[2:, 8:57]  # Extract from Columns 9 to 57, Row 3 onwards

# Ensure pressure values are numeric
pressure_values = pressure_values.apply(pd.to_numeric, errors='coerce')

# Function to calculate Cp from pressure using q_inf
def calculate_cp(pressure, q_inf):
    return pressure / q_inf

# Function to generate Cp vs Position graph for a given angle of attack
def plot_cp_vs_position(angle):
    # Debugging: Check if the requested angle is present
    print(f"Searching for angle: {angle}")
    
    # Find the row where the angle of attack matches
    matching_rows = angles_of_attack[angles_of_attack == angle]
    
    if matching_rows.empty:
        print(f"Error: Angle of attack {angle} not found.")
        return

    # Get the row index where the angle of attack matches
    angle_row = matching_rows.index[0]
    
    # Extract the pressure values for the corresponding angle
    pressures_at_angle = pressure_values.iloc[angle_row - 2]  # Adjust for zero-based index
    
    # Ensure the length of pressures_at_angle matches the number of sensor positions
    if len(pressures_at_angle) != len(sensor_positions):
        print(f"Warning: Pressure values length ({len(pressures_at_angle)}) doesn't match sensor positions length ({len(sensor_positions)}).")
        return
    
    # Calculate Cp values for each pressure
    cp_values = pressures_at_angle.apply(lambda p: calculate_cp(p, q_inf))
    
    # Create the Cp vs Position plot
    plt.figure(figsize=(10, 6))
    plt.plot(sensor_positions, cp_values, marker='o', linestyle='-', color='b')
    plt.title(f'Cp vs Position for Angle of Attack = {angle}°')
    plt.xlabel('Sensor Position (m)')
    plt.ylabel('Cp (Coefficient of Pressure)')
    
    # Customize x-axis with specified ticks
    plt.xticks(ticks=range(0, 101, 10))  # Custom x-ticks from 0 to 100 with a step of 10
    plt.xlim(0, 100)  # Set x-axis limits to 0-100 for better readability
    
    plt.grid(True)
    plt.show()

# Example: Plot Cp vs Position for a specific angle of attack (e.g., 5 degrees)
plot_cp_vs_position(5)
