file_path = "path/to/your/file.txt"

# Read the contents of the file
with open(file_path, "r") as file:
    lines = file.readlines()

# Remove newline characters and strip leading/trailing whitespaces from each line
lines = [line.strip() for line in lines]

# Process the lines as needed
for line in lines:
    # Do something with each line
    print(line)

# Write the remaining lines back to the file
with open(file_path, "w") as file:
    file.writelines(lines)