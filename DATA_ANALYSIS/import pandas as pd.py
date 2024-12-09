import pandas as pd

# Load the Excel data (sensor positions)
excel_data = pd.read_excel('DATA_ANALYSIS/PPS.xlsx', header=None)

# Extract sensor positions from Column B, Row 3 to Row 51 (adjusting for zero-indexing)
sensor_positions = excel_data.iloc[3:52, 1]  # Rows 3 to 51, Column B

# Display the sensor positions to verify
print(sensor_positions)
