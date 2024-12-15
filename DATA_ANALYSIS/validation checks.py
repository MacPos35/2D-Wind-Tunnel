import pandas as pd
import numpy as np
from cm_calculations import cm_calc, calculate_cp

# Constants
q_inf = 335.7613443  # Free-stream dynamic pressure (Pa)

# Validation function for C_M calculation
def validate_cm_check():
    """Validation for C_M calculations using cm_calculations.py functions."""

    # Test data (manual setup)
    sensor_positions = np.array([0.1, 0.2, 0.3, 0.4, 0.5])  # Example normalized x positions
    z_positions = np.array([0.05, 0.1, 0.0, -0.1, -0.05])    # Corresponding z positions
    cp_values = np.array([-0.2, -0.1, 0.0, 0.1, 0.2])        # Example Cp values

    # Example angle of attack
    angle = -6.0

    # Validate alignment
    if len(sensor_positions) != len(cp_values):
        print("Error: Sensor positions and Cp values length mismatch.")
        return

    # Calculate C_M
    try:
        cm = cm_calc(angle, split_point=None)
        print(f"Validation Result:\nAngle of Attack: {angle} degrees, Calculated C_M: {cm:.6f}")
    except Exception as e:
        print(f"Error during C_M calculation: {e}")

if __name__ == "__main__":
    validate_cm_check()

