import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

OUTPUT_TO_FILE = True
SHOW_PLOT = False

def exponential_func(x, y0, K):
    return y0 * np.exp(-x / K)

def exponential_fit(x, y):
    def linear_func(x, ln_y0, inv_K):
        return ln_y0 + inv_K * x

    mask = np.isfinite(y)
    x_valid = x[mask]
    y_valid = y[mask]

    ln_y = np.log(y_valid)
    try:
        popt, _ = curve_fit(linear_func, x_valid, ln_y, bounds=(-np.inf, np.inf))
    except ValueError as e:
        print("Error in curve_fit:", e)
        print("x_valid:", x_valid)
        print("ln_y:", ln_y)
        return None, None

    ln_y0_fit, inv_K_fit = popt
    y0_fit = np.exp(ln_y0_fit)
    K_fit = -1 / inv_K_fit

    y_fit = exponential_func(x, y0_fit, K_fit)

    residuals = y_valid - y_fit[mask]
    ss_res = np.sum(residuals**2)
    ss_tot = np.sum((y_valid - np.mean(y_valid))**2)
    r_squared = 1 - (ss_res / ss_tot)

    return (y0_fit, K_fit), r_squared

def read_data(file_name):
    x_values = []
    residue_data = []

    with open(file_name, 'r') as file:
        for line in file:
            values = line.strip().split()
            if len(values) > 0:  # Check if values list is not empty
                residue_name = float(values[0])  # Convert residue name to float
                data_values = [float(value) for value in values[1:]]  # Convert data values to float
                residue_data.append((residue_name, data_values))  # Append to residue_data
                if not x_values:  # If x_values is empty, populate it based on the number of data values
                    x_values = data_values

    return x_values, residue_data

def plot_fit(x, y, y_fit, residue_name, r_squared):
    plt.plot(x, y, 'ko', label='Data')
    plt.plot(x, y_fit, 'b-', label=f'Fit: y = {y_fit[0]:.2f} * exp(-x / {y_fit[1]:.2f})')
    plt.legend()
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title(f'Fit for Residue {residue_name} (R^2 = {r_squared:.4f})')
    plt.show()

def main():
    file_name = input("Enter the name of the data file: ")
    x_values, residue_data = read_data(file_name)

    if len(residue_data) < 1:
        print("Insufficient data to plot. At least 1 residue is required.")
        return

    for residue_name, y_values in residue_data:
        x = np.array(x_values)
        y = np.array(y_values)

        # Sort the values in ascending order
        sorted_indices = np.argsort(x)
        x = x[sorted_indices]
        y = y[sorted_indices]

        # Non-linear Fit
        fit_params, r_squared = exponential_fit(x, y)
        if fit_params is None or r_squared is None:
            continue
        if SHOW_PLOT:
            plot_fit(x, y, exponential_func(x, *fit_params), residue_name, r_squared)
        if OUTPUT_TO_FILE:
                with open("output_" + file_name, 'a') as file:
                    file.write(f"Residue {int(residue_name)}: Fitted parameters - y0 = {fit_params[0]:.4f}, K = {fit_params[1]:.4f}, R^2 = {r_squared:.4f}\n")
        print(f"Residue {int(residue_name)}: Fitted parameters - y0 = {fit_params[0]:.4f}, K = {fit_params[1]:.4f}, R^2 = {r_squared:.4f}")

if __name__ == '__main__':
    main()
