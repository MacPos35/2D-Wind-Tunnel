import pandas as pd
import numpy as np

# Constants
q_inf = 335.7613443  # Free-stream dynamic pressure (Pa)

# Step 1: Load airfoil geometry
def load_airfoil_geometry(file_path, sheet_name="Sheet1", usecols="B:C"):
    airfoil_data = pd.read_excel(file_path, sheet_name=sheet_name, header=1, usecols=usecols)
    airfoil_data.columns = ['x', 'z']
    x_coords = airfoil_data['x'].to_numpy()
    z_coords = airfoil_data['z'].to_numpy()
    return x_coords, z_coords

# Step 2: Split into upper and lower surfaces
def split_airfoil_surfaces(x_coords, z_coords):
    leading_edge_index = np.argmin(x_coords)
    x_upper = x_coords[:leading_edge_index + 1][::-1]
    z_upper = z_coords[:leading_edge_index + 1][::-1]
    x_lower = x_coords[leading_edge_index:]
    z_lower = z_coords[leading_edge_index:]
    return x_upper, z_upper, x_lower, z_lower

# Step 3: Load sensor data
def load_sensor_data(file_path):
    sensor_data = pd.read_excel(file_path, header=None)
    x_positions = sensor_data.iloc[2:52, 1].to_numpy() / 100.0
    z_positions = sensor_data.iloc[2:52, 2].to_numpy()
    return x_positions, z_positions

# Step 4: Load pressure data
def load_pressure_data(file_path):
    pressure_data = pd.read_csv(file_path, sep="\t", header=None)
    angles_of_attack = pd.to_numeric(pressure_data.iloc[2:, 2], errors='coerce')  # Convert to numeric
    pressure_values = pressure_data.iloc[2:, 8:57].apply(pd.to_numeric, errors='coerce')
    return angles_of_attack, pressure_values

# Step 5: Calculate Cp values
def calculate_cp(pressure, q_inf):
    return pressure / q_inf

# Step 6: Slope calculation
def calculate_slope(x_surface, z_surface, target_x):
    """
    Calculate the slope (dz/dx) at a specific x-coordinate.
    Handles out-of-bound cases by using the nearest valid slope.
    """
    # For points before the first segment, use the first segment's slope
    if target_x < x_surface[0]:
        return (z_surface[1] - z_surface[0]) / (x_surface[1] - x_surface[0])

    # For points after the last segment, use the last segment's slope
    elif target_x > x_surface[-1]:
        return (z_surface[-1] - z_surface[-2]) / (x_surface[-1] - x_surface[-2])

    # For in-bounds points, find the appropriate segment and calculate slope
    for i in range(1, len(x_surface)):
        if x_surface[i - 1] <= target_x <= x_surface[i]:
            return (z_surface[i] - z_surface[i - 1]) / (x_surface[i] - x_surface[i - 1])

    # If somehow no segment is found (unlikely), raise an error
    raise ValueError(f"Target x ({target_x}) is out of bounds for the surface.")

# Step 7: Tangential coefficient calculation
def ct_calc(angle, cp_values, x_coords, z_coords, sensor_positions, sensor_positions_z):
    """
    Calculate tangential force coefficient (C_T) for a given angle of attack.

    Arguments:
    angle : float
        Angle of attack (AoA).
    cp_values : array-like
        Pressure coefficient values (converted to NumPy array).
    x_coords, z_coords : array-like
        Airfoil coordinates for the current case.
    sensor_positions : array-like
        Sensor positions corresponding to Cp values.
    sensor_positions_z : array-like
        Sensor z (vertical) positions corresponding to the positions.

    Returns:
    float
        Tangential force coefficient (C_T).
    """
    # Split airfoil geometry into upper and lower surfaces
    x_upper, z_upper, x_lower, z_lower = split_airfoil_surfaces(x_coords, z_coords)

    # Initialize integrands and corresponding valid x-positions
    x_positions_upper = []  # Valid x-positions for upper surface
    x_positions_lower = []  # Valid x-positions for lower surface
    integrand_upper = []    # Integrand for upper surface
    integrand_lower = []    # Integrand for lower surface

    for i, x in enumerate(sensor_positions):
        cp = cp_values[i]

        # Determine slope based on z position
        if sensor_positions_z[i] > 0:  # Upper surface
            try:
                slope = calculate_slope(x_upper, z_upper, x)
                integrand_upper.append(cp * slope)
                x_positions_upper.append(x)  # Store valid x position
            except ValueError:
                print(f"Warning: Sensor position x={x} is out of bounds for the upper surface.")
        elif sensor_positions_z[i] < 0:  # Lower surface
            try:
                slope = calculate_slope(x_lower, z_lower, x)
                integrand_lower.append(cp * slope)
                x_positions_lower.append(x)  # Store valid x position
            except ValueError:
                print(f"Warning: Sensor position x={x} is out of bounds for the lower surface.")

    # Perform integration using only valid x-positions
    upper_surface = np.trapz(integrand_upper, x_positions_upper)
    lower_surface = np.trapz(integrand_lower, x_positions_lower)

    # Compute tangential coefficient
    ct = lower_surface - upper_surface
    return ct

# Main script
if __name__ == "__main__":
    # File paths
    airfoil_file = 'DATA_ANALYSIS/AIRFOIL_COORDINATES.xlsx'
    sensor_file = 'DATA_ANALYSIS/PPS.xlsx'
    pressure_file = 'DATA_ANALYSIS/raw_2d.txt'

    # Load data
    x_coords, z_coords = load_airfoil_geometry(airfoil_file)
    sensor_positions, sensor_positions_z = load_sensor_data(sensor_file)
    angles_of_attack, pressure_values = load_pressure_data(pressure_file)

    # Loop through angles of attack and calculate C_T
    alpha_array = []
    ct_array = []

    for angle_index, angle in enumerate(angles_of_attack):
        cp_values = calculate_cp(pressure_values.iloc[angle_index].to_numpy(), q_inf)
        ct = ct_calc(angle, cp_values, x_coords, z_coords, sensor_positions, sensor_positions_z)
        alpha_array.append(angle)
        ct_array.append(ct)

    # Print results
    for alpha, ct in zip(alpha_array, ct_array):
        print(f"Angle of Attack: {float(alpha):.2f} degrees, C_T: {ct:.6f}")