SAVE_TO_FILE = True
DEFAULT_FILENAME = False

# Prompt the user to enter the file names
rox_file_name = input("Enter the file name for Rox data: ")
red_file_name = input("Enter the file name for red data: ")

# Read the Rox data file
with open(rox_file_name, 'r') as rox_file:
    rox_lines = rox_file.readlines()

# Read the red data file
with open(red_file_name, 'r') as red_file:
    red_lines = red_file.readlines()

rox_data = {}
red_data = {}

# Process the Rox data
for line in rox_lines:
    if line.startswith("Residue"):
        residue_number = int(line.split(":")[0].split(" ")[1])
        parameters = line.split(":")[1].split(",")

        y0 = float(parameters[0].split("=")[1].strip())
        K = float(parameters[1].split("=")[1].strip())
        R2 = float(parameters[2].split("=")[1].strip())

        if K != 0:  # Avoid division by zero
            rox_1k = 1 / K
            rox_data[residue_number] = rox_1k

# Process the red data
for line in red_lines:
    if line.startswith("Residue"):
        residue_number = int(line.split(":")[0].split(" ")[1])
        parameters = line.split(":")[1].split(",")

        y0 = float(parameters[0].split("=")[1].strip())
        K = float(parameters[1].split("=")[1].strip())
        R2 = float(parameters[2].split("=")[1].strip())

        if K != 0:  # Avoid division by zero
            red_1k = 1 / K
            red_data[residue_number] = red_1k

if SAVE_TO_FILE:
    if DEFAULT_FILENAME:
        file_name = "PRE2_RES.txt"
    else:
        file_name = input("Please enter the filename of the result: ")
        if not file_name.endswith('.txt'):
            file_name = file_name + '.txt'
        
# Calculate R_pre
for residue_number in rox_data.keys():
    if residue_number in red_data:
        rox_1k = rox_data[residue_number]
        red_1k = red_data[residue_number]
        difference = rox_1k - red_1k
        if SAVE_TO_FILE:
            with open(file_name, "a") as file:
                file.write(f"Residue {residue_number}: Difference = {difference:.4f}\n")
        else:
            print(f"Residue {residue_number}: Difference = {difference:.4f}")
    else:
        if SAVE_TO_FILE:
            with open(file_name, "a") as file:
                file.write(f"Residue {residue_number} not found in the red data.\n")
        else:
            print(f"Residue {residue_number} not found in the red data.")

