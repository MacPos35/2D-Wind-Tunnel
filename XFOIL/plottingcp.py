import numpy as np
import scipy as sp 
import matplotlib.pyplot as plt 

file_path = "XFOIL\Cpvalues.cp"
try: 
    data=np.loadtxt(file_path, skiprows=1)
except Exception as e :
    print(f"Error reading the file: {e}")
    exit()

x_c=0
Cp=1

x_c_data=data[:,x_c]
Cp_data=data[:,Cp]

plt.figure(figsize=(10, 6))
plt.plot(x_c_data, -Cp_data, label="Cpvsx")
plt.xlabel("X-axis")
plt.ylabel("CP-axis")
plt.title("Cp vs x plot")
plt.legend()
plt.grid(True)
plt.show()