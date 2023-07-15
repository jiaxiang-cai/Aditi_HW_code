import pandas as pd
import matplotlib.pyplot as plt

# Read the Excel file
file_name = 'DNAJC7_buffers_n_pH.xls'
df_temp = pd.read_excel(file_name, sheet_name='Melt Region Temperature Data', header=None, skiprows=8)
df_deriv = pd.read_excel(file_name, sheet_name='Melt Region Derivative Data', header=None, skiprows=8)

# Extract the desired data for plotting
data_sets = [(1, 12), (13, 24), (25, 37)]  # Start and end rows for each plot
plots = []

for start_row, end_row in data_sets:
    # Get the sample names
    sample_names = df_temp.iloc[start_row-1:end_row-1, 1].tolist()
    
    # Get the melting temperatures (x-axis data)
    x_data = df_temp.iloc[start_row-1:end_row-1, 4:234].values.T
    
    # Get the fluorescence values (y-axis data)
    y_data = df_deriv.iloc[start_row-1:end_row-1, 4:234].values.T
    
    # Create the plot
    plt.figure()
    for i in range(len(sample_names)):
        plt.plot(x_data[:, i], y_data[:, i], label=sample_names[i])
    
    # Set plot title and labels
    plt.title(f'Plot {len(plots)+1}')
    plt.xlabel('Melting Temperatures')
    plt.ylabel('Fluorescence Values')
    
    # Add legend
    plt.legend()
    
    # Set x-axis limits to show all values
    plt.xlim(left=x_data.min(), right=x_data.max())
    
    # Add the plot to the list
    plots.append(plt)

# Show all the plots
plt.show()
