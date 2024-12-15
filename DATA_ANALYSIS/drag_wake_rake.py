import pandas as pd
import numpy as np
from scipy.integrate import quad

# Load the Excel sheet provided by the user
file_path = 'DATA_ANALYSIS/wake_velocities.xlsx'
data = pd.read_excel(file_path, header=2)

# Extract AoA values and spanwise locations
aoa_column = 'Location (mm)'  # The first column contains AoA values
aoa_values = data[aoa_column][1:]  # Exclude the header row
spanwise_locations = [col for col in data.columns if col != aoa_column]  # All other columns are spanwise locations

# Convert the spanwise locations to numeric for integration
spanwise_locations = list(map(float, spanwise_locations))

# Create a dictionary of velocity profiles for each AoA
velocity_profiles = data.iloc[1:, 1:].set_index(data[aoa_column][1:])

# Load the Excel sheet provided by the user pressures
file_path = 'DATA_ANALYSIS/wake_pressures.xlsx'
data = pd.read_excel(file_path, header=2)

# Extract AoA values and spanwise locations
aoa_column_p = 'Location (mm)'  # The first column contains AoA values
aoa_values_p = data[aoa_column][1:]  # Exclude the header row
spanwise_locations_p = [col for col in data.columns if col != aoa_column]  # All other columns are spanwise locations

# Convert the spanwise locations to numeric for integration
spanwise_locations_p = list(map(float, spanwise_locations_p))

# Create a dictionary of pressure profiles for each AoA
pressure_profiles = data.iloc[1:, 1:].set_index(data[aoa_column][1:])

# Define constants
rho = 1.181615446 # Air density, replace with actual value

# Function to calculate drag for a given AoA
def calculate_drag(aoa):
    velocity_profile = velocity_profiles.loc[aoa]
    pressure_profile = pressure_profiles.loc[aoa]

    def U_infinity():
        return 23.8392323  # Freestream velocity (m/s)

    def p_infinity():
        return 99831.30769  # Freestream pressure (Pa)

    def first_term(location_start, location_end):
        # Find the nearest spanwise location indices
        location_start_idx = np.abs(np.array(spanwise_locations) - location_start).argmin()
        location_end_idx = np.abs(np.array(spanwise_locations) - location_end).argmin()

        # Extract velocities at segment bounds
        U_start = float(velocity_profile.iloc[location_start_idx])
        U_end = float(velocity_profile.iloc[location_end_idx])

        # Average velocity over the segment and return the momentum integrand
        return (U_infinity() - ((U_start + U_end) / 2)) * ((U_start + U_end) / 2) * (location_end - location_start)

    def second_term(location_start, location_end):
        # Find the nearest spanwise location indices
        location_start_idx = np.abs(np.array(spanwise_locations_p) - location_start).argmin()
        location_end_idx = np.abs(np.array(spanwise_locations_p) - location_end).argmin()

        # Extract pressures at segment bounds
        p_start = float(pressure_profile.iloc[location_start_idx])
        p_end = float(pressure_profile.iloc[location_end_idx])

        # Approximate pressure integral using trapezoidal rule
        return ((p_infinity() - ((p_start + p_end) / 2)) * (location_end - location_start))

    # Compute total drag
    total_drag = 0
    for i in range(len(spanwise_locations) - 1):
        location_start = spanwise_locations[i]
        location_end = spanwise_locations[i + 1]

        # Compute contributions from both terms
        segment_drag = rho * first_term(location_start, location_end)
        pressure_drag = second_term(location_start, location_end)
        total_drag += segment_drag + pressure_drag

    return total_drag

# Iterate over AoAs and compute drag
aoa_range = [-6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10.5, 11, 11.5, 12, 12.5, 13, 13.5, 14, 14.5, 15, 15.5, 16] 
drag_results = [(aoa, calculate_drag(aoa)) for aoa in aoa_range]

# Output the results
for aoa, drag in drag_results:
    print(f"AoA: {aoa}°, Drag (D): {drag}")
