import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Constants
c = 0.16  # m
q_inf = 335.7613443  # Pa
p_inf = 99495.54635  # Pa

# Read position data
positions = pd.read_excel('DATA_ANALYSIS/PPS.xlsx', skiprows=2, usecols=[1, 2], sheet_name=1)
positions = positions.to_numpy()

# Read raw pressure data
with open('DATA_ANALYSIS/raw_2d.txt', 'r') as f:
    lines = f.readlines()
data = [line.strip().split('\t') for line in lines[2:]]

# Store pressures in a dictionary for each PXXX
columns = {}
for i in range(49):  # There are 49 pressure points
    column_name = f'P{i+1:03d}'
    columns[column_name] = np.array([float(row[i+8]) for row in data])

# Calculate deltaP_bar (change in pressure)
deltaP_bar = np.array([float(row[3]) for row in data])  # Assuming the 4th column holds deltaP_bar

# Extract angle of attack (alphas)
alphas = np.array([float(row[2]) for row in data])

# Calculate C_p for each PXXX and store it in a dictionary
cp_data = {}
for column_name, pressures in columns.items():
    # Correct formula for C_p
    cp_values = (deltaP_bar - pressures) / q_inf
    cp_data[column_name] = cp_values

# Combine positions with C_p data
cp_positions = pd.DataFrame(positions, columns=['X', 'Y'])  # Add X, Y positions
cp_values = pd.DataFrame(cp_data)  # Add C_p values for each PXXX

# Combine positions and C_p values into a single DataFrame
combined_data = pd.concat([cp_positions, cp_values], axis=1)

# Example: Save combined data to a file for later analysis
combined_data.to_csv('DATA_ANALYSIS/cp_results.csv', index=False)

print("C_p values computed and combined with positions. Data saved to 'cp_results.csv'.")

# Function to plot C_p vs alpha for a specified range of PXXX points
def plot_cp_vs_alpha(pressure_points, alphas, columns, deltaP_bar, q_inf):
    # Create 6 subplots (2 rows x 3 columns)
    fig, ax = plt.subplots(2, 3, figsize=(18, 12))

    # Flatten the ax array for easy indexing
    ax = ax.flatten()

    # Loop through the selected pressure points (up to 6 plots)
    for i, pressure_point in enumerate(pressure_points):
        if pressure_point in columns:
            # Extract pressure data for the selected PXXX
            pressure_data = columns[pressure_point]

            # Calculate C_p for the selected PXXX using the correct formula
            cp_values = (deltaP_bar - pressure_data) / q_inf

            # Plot C_p vs alpha
            ax[i].plot(alphas, cp_values, label=f'{pressure_point} - C_p vs α', color='blue')
            ax[i].set_xlabel('Angle of Attack (α)')
            ax[i].set_ylabel('C_p')
            ax[i].set_title(f'Variation of C_p with α for {pressure_point}')
            ax[i].legend()
            ax[i].grid(True)
        else:
            # If a pressure point is not found, hide the subplot
            ax[i].axis('off')

    plt.tight_layout()
    plt.show()

# Example usage: choose a range of pressure points (e.g., 'P015' to 'P020')
pressure_points_to_plot = ['P001', 'P002', 'P003', 'P004', 'P005', 'P006']
plot_cp_vs_alpha(pressure_points_to_plot, alphas, columns, deltaP_bar, q_inf)
