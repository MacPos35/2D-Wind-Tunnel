import pandas as pd
import matplotlib.pyplot as plt

# Define the path to your text file and Excel file
text_file_path = 'DATA_ANALYSIS/raw_2d.txt'
excel_file_path = 'DATA_ANALYSIS/PPS.xlsx'

# Load the tab-separated text file with two header rows
data = pd.read_csv(text_file_path, sep='\t', header=2)

# Preview the first few rows of the data to check if it's correctly loaded
print(data.head())

# Load the sensor locations from the Excel file using index (column index 1 corresponds to 'B')
sensor_data = pd.read_excel(excel_file_path, header=2, usecols=[1])  # Column 'B' corresponds to index 1
sensor_locations = sensor_data.iloc[:, 0]  # Extract the data from the first column

# Print the sensor locations to verify
print(sensor_locations)

q_inf = 335.7613443  # Pa (reference pressure)

# Specify the angle of attack you want to analyze (e.g., 5 degrees)
angle_of_attack = 5

# Filter the data for the specified angle of attack (angle of attack is in column 3 of the text file, which is index 2)
filtered_data = data[data.iloc[:, 2] == angle_of_attack]

# Extract pressure values from columns 9 to 57 (which correspond to P001 to P049)
pressure_values = filtered_data.iloc[:, 8:57]  # Columns 9 to 57 (index starts from 0)

# Compute Cp for each sensor
Cp_values = pressure_values / q_inf

# Add the Cp values to the filtered data
filtered_data = filtered_data.join(Cp_values)

# Check the resulting data
print(filtered_data[['xcords', 'Alpha'] + list(pressure_values.columns)])

# Plot Cp vs. sensor location
plt.figure(figsize=(10, 6))

# Loop through each column of Cp values (P001 to P049) and plot
for sensor in Cp_values.columns:
    plt.plot(sensor_locations, filtered_data[sensor], label=sensor)

# Set plot labels and title
plt.title(f'Pressure Coefficient Distribution at {angle_of_attack}° Angle of Attack')
plt.xlabel('Normalized Chord Position (x/c)')
plt.ylabel('Pressure Coefficient (C_p)')
plt.grid(True)

# Add a legend
plt.legend(title='Sensors', bbox_to_anchor=(1.05, 1), loc='upper left')  # To handle the legend outside the plot
plt.tight_layout()  # To avoid clipping of labels
plt.show()
