import numpy as np
import scipy as sp 
import matplotlib.pyplot as plt 

#file_path = "Cpvaluesinviscid.cp"
#file_path = "Cpviscousflow.cp"
#file_path = "Cpvaluesexperimental.cp"
#load the experimental data
file_path1 = "Cpvaluesexperimental.cp"
try: 
    data1=np.loadtxt(file_path1, skiprows=1)
except Exception as e :
    print(f"Error reading the file: {e}")
    exit()
x_c=0
Cp=1

x_c_data1=data1[:,x_c]
Cp_data1=data1[:,Cp]
#load the xfoil data
file_path2 = "Cpvaluesinviscid.cp"
try: 
    data2=np.loadtxt(file_path2, skiprows=1)
except Exception as e :
    print(f"Error reading the file: {e}")
    exit()
x_c=0
Cp=1

x_c_data2=data2[:,x_c]
Cp_data2=data2[:,Cp]

plt.figure(figsize=(10, 6))
plt.plot(x_c_data1, Cp_data1, label="Experimental")
plt.plot(x_c_data2, Cp_data2, label="XFOIL")
plt.gca().invert_yaxis()
plt.xlabel("X-axis")
plt.ylabel("CP-axis")
plt.title("Cp vs x plot")
plt.legend()
plt.grid(True)
plt.show()