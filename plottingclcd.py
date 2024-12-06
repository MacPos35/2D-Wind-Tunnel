import numpy as np
import scipy as sp 
import matplotlib.pyplot as plt 

file_path = "CLCDcurvesPiotr.dat"

try: 
    data=np.loadtxt(file_path, skiprows=12)
except Exception as e :
    print(f"Error reading the file: {e}")
    exit()

alfa_column=0
cl_column=1
cd_column=2

alfa_data=data[:,alfa_column]
cl_data=data[:,cl_column]
cd_data=data[:,cd_column]

fig,axs = plt.subplots(2,1,figsize=(8,10))

axs[0].scatter(alfa_data, cl_data, label="Cl alfa curve", color="blue")
axs[0].set_title("Cl alfa curve")
axs[0].set_xlabel("alfa")
axs[0].set_ylabel("Cl")
axs[0].legend()
axs[0].grid(True)

# Step 4: Plot data on the second subplot
axs[1].scatter(cd_data, cl_data, label="ClCd", color="green")
axs[1].set_title("Drag polar")
axs[1].set_xlabel("CD")
axs[1].set_ylabel("CL")
axs[1].legend()
axs[1].grid(True)

# Step 5: Adjust layout and show the plots
plt.tight_layout()  # Adjusts spacing between subplots
plt.show()
    

