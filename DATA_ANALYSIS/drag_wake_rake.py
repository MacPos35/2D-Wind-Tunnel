import pandas as pd
import numpy as np
from scipy.integrate import quad

# Load the Excel sheet provided by the user
file_path = '/DATA_ANALYSIS/wake_velocities.xlsx'
data = pd.read_excel(file_path, header=2)

# Clean and process the data
spanwise_locations = [col for col in data.columns if not pd.isnull(col) and col != 'Alpha (degrees)']
aoa_values = data['Alpha (degrees)'][1:]  # Extract AoA values (skip header row)

# Extract spanwise location in mm and convert to float for integration
spanwise_locations = list(map(float, spanwise_locations))

# Create a dictionary of velocity profiles for each AoA
velocity_profiles = data.iloc[1:, 1:].set_index(data['Alpha (degrees)'][1:])

# Define constants
rho = 1.225  # Air density, replace with actual value

# Function to calculate drag for a given AoA
def calculate_drag(aoa):
    velocity_profile = velocity_profiles.loc[aoa]

    def U_infinity():
        return 23.8392323  # Freestream velocity, replace with actual value

    def p_infinity():
        return 100189.3662  # Freestream pressure, replace with actual value

    def first_term(y, location_start, location_end):
        """
        Calculate the first term of the drag integral over a segment.
        """
        location_index_start = np.abs(np.array(spanwise_locations) - location_start).argmin()
        location_index_end = np.abs(np.array(spanwise_locations) - location_end).argmin()

        U_start = velocity_profile.iloc[location_index_start]
        U_end = velocity_profile.iloc[location_index_end]
        return (U_infinity() - U_start) * U_end

    total_drag = 0
    for i in range(len(spanwise_locations) - 1):
        location_start = spanwise_locations[i]
        location_end = spanwise_locations[i + 1]
        segment_drag = quad(first_term, location_start, location_end, args=(location_start, location_end))[0]
        total_drag += rho * segment_drag

    return total_drag

# Iterate over AoAs and compute drag
aoa_range = [-6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10.5, 11, 11.5, 12, 12.5, 13, 13.5, 14] 
drag_results = [(aoa, calculate_drag(aoa)) for aoa in aoa_range]

# Output the results
for aoa, drag in drag_results:
    print(f"AoA: {aoa}°, Drag (D): {drag}")
