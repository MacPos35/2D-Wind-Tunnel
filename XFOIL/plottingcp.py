import numpy as np
import matplotlib.pyplot as plt

# --- Load Cp data ---
file_path = "XFOIL/Cpvalues.cp"
try:
    cp_data = np.loadtxt(file_path, skiprows=1)
except Exception as e:
    print(f"Error reading the Cp file: {e}")
    exit()

x_c = 0
Cp = 1

x_c_data = cp_data[:, x_c]
Cp_data = cp_data[:, Cp]

# --- Load Airfoil data ---
try:
    airfoil_data = np.loadtxt("XFOIL/SD6060-104-88_180.dat", skiprows=1)
except Exception as e:
    print(f"Error reading the airfoil file: {e}")
    exit()

x = airfoil_data[:, 0]
y = airfoil_data[:, 1]

# Find the index of the point closest to x = 0
idx_x0 = np.argmin(np.abs(x))

# Shift x so the point closest to x = 0 becomes the origin
x_shifted = x - x[idx_x0]

# Shift y so the y-value at x = 0 becomes 0
y_shifted = y - y[idx_x0]

# Normalize x to [0, 1]
x_normalized = x_shifted / (np.max(x_shifted) - np.min(x_shifted))

# Normalize y to [0, 1]
y_normalized = y_shifted / (np.max(y_shifted) - np.min(y_shifted))

# Normalize Cp data (optional, for alignment)
x_c_normalized = (x_c_data - np.min(x_c_data)) / (np.max(x_c_data) - np.min(x_c_data))

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(x_normalized, y_normalized, label='Normalized Airfoil Data', color='tab:blue')
plt.plot(x_c_normalized, -Cp_data, label="Cp vs x", color='tab:orange')

plt.gca().invert_yaxis()  # Invert y-axis for Cp convention
plt.xlabel("x/c [-]")
plt.ylabel("Cp [-]")
plt.title("Cp vs x/c")
plt.legend()
plt.grid()
plt.show()
