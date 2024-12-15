import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Constants
q_inf = 335.7613443  # Free-stream dynamic pressure (Pa)

# Load Excel data (sensor positions)
excel_data = pd.read_excel('DATA_ANALYSIS/PPS.xlsx', header=None)
# Extract sensor positions from Column B, Row 3 to Row 51 (adjusting for zero-indexing)
sensor_positions = excel_data.iloc[2:52, 1]  # Rows 2 to 51, Column B
sensor_positions_y = excel_data.iloc[2:52, 2]

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
# Function to generate Cp vs Position graph for a given angle of attack
def plot_cp_vs_position(angle, split_point=None):
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
    cp_values = pressures_at_angle.apply(lambda p: calculate_cp(p, q_inf)).to_numpy()  # Convert to numpy array
    sensor_positions_np = sensor_positions.to_numpy()  # Convert positions to numpy array

    # Set the split point (choose somewhere near the middle or manually set)
    if split_point is None or split_point >= len(sensor_positions):
        split_point = len(sensor_positions) // 2  # Default split at the midpoint of the array

    # Ensure that the split point is a valid index
    split_point = min(max(0, split_point), len(sensor_positions) - 1)

    # Split data into two parts for plotting
    positions_part1 = sensor_positions_np[:split_point]
    positions_part2 = sensor_positions_np[split_point:]
    cp_part1 = cp_values[:split_point]
    cp_part2 = cp_values[split_point:]

    # Create the Cp vs Position plot
    plt.figure(figsize=(10, 6))

    # Plot the first part of the data
    plt.plot(positions_part1, cp_part1, marker='o', linestyle='-', color='b', label='Cp curve')

    # Plot the second part of the data
    plt.plot(positions_part2, cp_part2, marker='o', linestyle='-', color='b')

    # Connect point 1 and point 26
    plt.plot(
        [sensor_positions_np[0], sensor_positions_np[25]],  # x-coordinates of points
        [cp_values[0], cp_values[25]],  # y-coordinates of points
        linestyle='-', color='b'
    )

    plt.title(f'Cp vs Position for Angle of Attack = {angle}°, Re = 2.5e5')
    plt.xlabel('Sensor Position (x/c) [%]')
    plt.ylabel('Cp (Coefficient of Pressure) [~]')

    # Calculate limits with added margin
    x_min, x_max = sensor_positions_np.min(), sensor_positions_np.max()
    y_min, y_max = cp_values.min(), cp_values.max()

    x_margin = (x_max - x_min) * 0.05  # 5% margin for x
    y_margin = (y_max - y_min) * 0.05  # 5% margin for y

    plt.xlim(x_min - x_margin, x_max + x_margin)
    plt.ylim(y_min - y_margin, y_max + y_margin)

    # Invert the y-axis for Cp plots
    plt.gca().invert_yaxis()

    # Add grid and spines for better visualization
    plt.grid(True)
    ax = plt.gca()
    ax.spines['top'].set_visible(True)
    ax.spines['right'].set_visible(True)
    ax.spines['bottom'].set_visible(True)
    ax.spines['left'].set_visible(True)

    # Adjust tick positions
    ax.xaxis.set_ticks_position('bottom')  # Place x-ticks on the bottom spine
    ax.yaxis.set_ticks_position('left')    # Place y-ticks on the left spine

    # Add the legend
    plt.legend()
    
    # Show the plot
    plt.show()

    # Calculate areas under the curve
    cp_u = np.where(sensor_positions_y > 0, cp_values, 0)
    cp_l = np.where(sensor_positions_y < 0, cp_values, 0)
    x_positions = sensor_positions / 100.0  # Convert sensor positions to x/c

    area_cpu = np.trapz(cp_u, x_positions)
    area_cpl = np.trapz(cp_l, x_positions)
    area_total = area_cpl - area_cpu

    print("Area Cp Upper:", area_cpu)
    print("Area Cp Lower:", area_cpl)
    print("Total Area:", area_total)





# Example: Plot Cp vs Position for a specific angle of attack (e.g., 5 degrees) and split point
plot_cp_vs_position(-5, split_point=25)  # Try changing the split_point value to test different splits
plot_cp_vs_position(0, split_point=25)
plot_cp_vs_position(5, split_point=25)
plot_cp_vs_position(10, split_point=25)
plot_cp_vs_position(15, split_point=25)