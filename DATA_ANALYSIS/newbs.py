import pandas as pd

# Constants
q_inf = 335.7613443  # Free-stream dynamic pressure (Pa)

# Load Excel data (sensor positions)
excel_data = pd.read_excel('DATA_ANALYSIS/PPS.xlsx', header=None)
sensor_positions = excel_data.iloc[2:52, 1]  # Rows 2 to 51, Column B

# Load text file data (angles of attack and pressure values)
text_data = pd.read_csv('DATA_ANALYSIS/raw_2d.txt', sep="\t", header=None)

# Extract angles of attack (starting from Column 3, Row 3 in text file)
angles_of_attack = text_data.iloc[2:, 2]
angles_of_attack = pd.to_numeric(angles_of_attack, errors='coerce')

# Extract pressure values (Columns 9 to 57 starting from Row 3 in text file)
pressure_values = text_data.iloc[2:, 8:57]
pressure_values = pressure_values.apply(pd.to_numeric, errors='coerce')

# Function to calculate Cp from pressure using q_inf
def calculate_cp(pressure, q_inf):
    return pressure / q_inf

# Create an empty DataFrame to store the Cp values
cp_data = {'Sensor Position': sensor_positions}

# Loop through each unique angle of attack and calculate the Cp values
for angle in angles_of_attack.unique():
    # Find the row where the angle of attack matches
    matching_rows = angles_of_attack[angles_of_attack == angle]
    
    if matching_rows.empty:
        print(f"Error: Angle of attack {angle} not found.")
        continue

    # Get the row index where the angle of attack matches
    angle_row = matching_rows.index[0]
    
    # Adjust the row for the data misalignment (assuming the data starts a few rows lower)
    # For example, if data starts 6 rows lower, adjust by `angle_row + 6`
    pressure_row = angle_row + 6  # Adjust this number based on your file structure
    
    # Extract the pressure values for the corresponding angle
    pressures_at_angle = pressure_values.iloc[pressure_row - 2]  # Adjust for zero-based index
    
    # Ensure the length of pressures_at_angle matches the number of sensor positions
    if len(pressures_at_angle) != len(sensor_positions):
        print(f"Warning: Pressure values length ({len(pressures_at_angle)}) doesn't match sensor positions length ({len(sensor_positions)}).")
        continue
    
    # Calculate Cp values for each pressure
    cp_values = pressures_at_angle.apply(lambda p: calculate_cp(p, q_inf))
    
    # Add Cp values to the DataFrame
    cp_data[f'Cp for {angle}°'] = cp_values

# Convert cp_data to DataFrame
final_cp_df = pd.DataFrame(cp_data)

# Save the DataFrame to a tab-separated values (TSV) file
output_file = 'Cp_values.csv'
final_cp_df.to_csv(output_file, sep=',', index=False)

print(f"Pressure coefficient values for all angles of attack have been saved to {output_file}")
