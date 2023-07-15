import pandas as pd

# Read the Excel file
file_name = 'DNAJC7_buffers_n_pH.xls'
df_temp = pd.read_excel(file_name, sheet_name='Melt Region Temperature Data', header=None, skiprows=8)
df_deriv = pd.read_excel(file_name, sheet_name='Melt Region Derivative Data', header=None, skiprows=8)

data_sets = [(1, 20), (21, 32), (33, 44)]  # Define the data set ranges

for start_row, end_row in data_sets:
    # Get the sample names
    sample_names = df_temp.iloc[start_row-1:end_row-1, 1].tolist()

    # Get the melting temperatures
    x_data = df_temp.iloc[start_row-1:end_row-1, 4:234].values.T

    # Get the fluorescence values (y-axis data)
    y_data = df_deriv.iloc[start_row-1:end_row-1, 4:234].values.T

    # Find the lowest value for each sample and its corresponding melting temperature
    lowest_values = []
    for i in range(len(sample_names)):
        sample = sample_names[i]
        x_values = x_data[:, i]
        y_values = y_data[:, i]
        lowest_index = y_values.argmin()
        lowest_value = y_values[lowest_index]
        lowest_temperature = x_values[lowest_index]
        lowest_values.append((sample, lowest_value, lowest_temperature))

    # Print the lowest value and corresponding melting temperature for each sample
    for sample, lowest_value, lowest_temperature in lowest_values:
        print(f"Sample: {sample} - Lowest Value: {lowest_value} - Melting Temperature: {lowest_temperature}")
