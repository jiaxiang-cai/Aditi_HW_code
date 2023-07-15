import re

def calculate_r(residue, difference, K, tau_c, w):
    difference_2 = difference
    if difference_2 == 0:
        return None  # Skip calculation if difference is zero
    
    r = ((K / difference_2) * (4 * tau_c + (3 * tau_c) / (1 + (w * tau_c)**2)))**(1/6)
    if isinstance(r, complex):
        return None  # Skip complex values of r
    return r

def parse_file(filename, tau_c, w):
    with open(filename, 'r') as file:
        content = file.read()

    pattern = r'Residue (\d+): Difference = (-?\d+\.\d+)'
    matches = re.findall(pattern, content)

    results = []
    for match in matches:
        residue = float(match[0])
        difference = float(match[1])
        r = calculate_r(residue, difference, K, tau_c, w)
        if r is not None:
            results.append((residue, r))

    return results

# Prompt the user to enter the file name and values for tau_c and w (frequency)
filename = input("Enter the file name: ")
tau_c = float(input("Enter the value for tau_c: "))
w = float(input("Enter the value for w (frequency in MHz):  "))

# Set the value for K
K = 1.23 * (10**-34)

results = parse_file(filename, tau_c, w)

# Sort results based on ascending r values
sorted_results = sorted(results, key=lambda x: x[1])

if sorted_results:
    for residue, r in sorted_results:
        r_meters = r / 100  # Convert from centimeters to meters
        print(f"Residue {residue}: r = {r_meters} meters")
else:
    print("No results found.")
