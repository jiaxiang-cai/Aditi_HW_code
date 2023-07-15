import pandas as pd
import matplotlib.pyplot as plt

# Load the data from Excel
file_name = 'DNAJC7_insuline_31_05_2023.xlsx'
sheet_name = 'Plate 1 - Sheet1'
time_range = 'B47:B300'  # Update the time range to a shorter range
sample_range = 'D47:H587'  # Update the sample range excluding P to T columns

df = pd.read_excel(file_name, sheet_name=sheet_name, usecols=[1] + list(range(3, 8)), skiprows=46)

# Extract the time column
time_column = df.iloc[:, 0]

# Select the shorter time range from the time column
time_column = time_column.iloc[:180]  # Update the number of rows to match the new time range

# Convert time column to string format
time_column = time_column.apply(lambda x: str(x))

# Set up the plot
plt.figure(figsize=(10, 6))

# Plot each sample (excluding P to T columns)
for column in df.columns[1:]:
    plt.plot(time_column, df[column][:180], marker='o', linestyle='-', markersize=4)  # Update the number of rows to match the new time range

# Add legends
plt.legend(df.columns[1:])

# Set labels and title
plt.xlabel('Time')
plt.ylabel('Turbidity')
plt.title('Turbidity vs Time')

# Set x-axis tick placement and labels
plt.xticks(range(0, len(time_column), 20), time_column[::20], rotation=90)

# Show the plot
plt.show()
