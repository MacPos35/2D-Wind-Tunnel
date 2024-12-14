import pandas as pd
import numpy as np

# General Part: Functions for processing airfoil geometry and calculating slopes
def load_airfoil_geometry(file_path, sheet_name="Sheet1", usecols="B:C"):
    """
    Load airfoil geometry from an Excel file.
    
    Arguments:
    file_path : str
        Path to the Excel file.
    sheet_name : str
        Name of the sheet in the Excel file (default: "Sheet1").
    usecols : str
        Columns to load (default: "B:C" for x and z).

    Returns:
    tuple
        x and z coordinates as NumPy arrays.
    """
    airfoil_data = pd.read_excel(file_path, sheet_name=sheet_name, header=1, usecols=usecols)
    airfoil_data.columns = ['x', 'z']  # Assign column names
    x_coords = airfoil_data['x'].to_numpy()
    z_coords = airfoil_data['z'].to_numpy()
    return x_coords, z_coords


def split_airfoil_surfaces(x_coords, z_coords):
    """
    Split airfoil geometry into upper and lower surfaces based on the leading edge.

    Arguments:
    x_coords : array-like
        x-coordinates of the airfoil geometry.
    z_coords : array-like
        z-coordinates of the airfoil geometry.

    Returns:
    tuple
        Upper and lower surfaces: (x_upper, z_upper, x_lower, z_lower).
    """
    leading_edge_index = np.argmin(x_coords)  # Find leading edge (minimum x)
    x_upper = x_coords[:leading_edge_index + 1][::-1]  # Upper surface (trailing to leading edge)
    z_upper = z_coords[:leading_edge_index + 1][::-1]
    x_lower = x_coords[leading_edge_index:]  # Lower surface (leading to trailing edge)
    z_lower = z_coords[leading_edge_index:]
    return x_upper, z_upper, x_lower, z_lower


# Main script
if __name__ == "__main__":
    # Load the airfoil geometry from the given dataset
    file_path = 'DATA_ANALYSIS/AIRFOIL_COORDINATES.xlsx'
    x_coords, z_coords = load_airfoil_geometry(file_path)

    # Split the airfoil into upper and lower surfaces
    x_upper, z_upper, x_lower, z_lower = split_airfoil_surfaces(x_coords, z_coords)

    # Calculate the slope (dz/dx) for one pair of adjacent points on the upper surface
    i = 1  # Pick the second point (index 1) and the first point (index 0) on the upper surface
    dz_dx = (z_upper[i] - z_upper[i - 1]) / (x_upper[i] - x_upper[i - 1])

    # Print the result without rounding
    print("Slope (dz/dx) between points:")
    print("Point 1:", x_upper[i - 1], z_upper[i - 1])
    print("Point 2:", x_upper[i], z_upper[i])
    print("Calculated Slope (dz/dx):", dz_dx)
