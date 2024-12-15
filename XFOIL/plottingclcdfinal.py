import numpy as np
import scipy as sp 
import matplotlib.pyplot as plt 

#file_path = "plotforcevisc.dat"
#file_path = "plotforceinviscid.dat"

#load data for the experimental data
file_path1 = "experimentaldata.dat"
try: 
    data1=np.loadtxt(file_path1, skiprows=12)
except Exception as e :
    print(f"Error reading the file: {e}")
    exit()

alfa_column=0
cl_column=1
cd_column=2

alfa_data1=data1[:,alfa_column]
cl_data1=data1[:,cl_column]
cd_data1=data1[:,cd_column]
#load XFOIL data (viscous or inviscid)
file_path2 = "plotforceinviscid.dat"
try: 
    data2=np.loadtxt(file_path2, skiprows=12)
except Exception as e :
    print(f"Error reading the file: {e}")
    exit()

alfa_column=0
cl_column=1
cd_column=2

alfa_data2=data2[:,alfa_column]
cl_data2=data2[:,cl_column]
cd_data2=data2[:,cd_column]

fig,axs = plt.subplots(2,1,figsize=(8,10))

axs[0].plot(alfa_data1, cl_data1, label="Experimental data", color="blue")
axs[0].plot(alfa_data2, cl_data2, label="XFOIL data", color="red")
axs[0].set_title("Cl alfa curve")
axs[0].set_xlabel("alfa")
axs[0].set_ylabel("Cl")
axs[0].legend()
axs[0].grid(True)

# Step 4: Plot data on the second subplot
axs[1].plot(cd_data1, cl_data1, label="XFOIL data", color="green")
axs[1].plot(cd_data2, cl_data2, label="Experimental data", color="purple")
axs[1].set_title("Drag polar")
axs[1].set_xlabel("CD")
axs[1].set_ylabel("CL")
axs[1].legend()
axs[1].grid(True)

# Step 5: Adjust layout and show the plots
plt.tight_layout()  # Adjusts spacing between subplots
plt.show()
    

