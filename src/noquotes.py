# Read the file
with open('Data/2023pb.csv', 'r') as file:
    lines = file.readlines()

# Remove quotes and save back
with open('Data/2023pb.csv', 'w') as file:
    for line in lines:
        file.write(line.strip('"\n') + '\n')