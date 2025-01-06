# Read the file
with open('Data/ProBowlers.csv', 'r') as file:
    lines = file.readlines()

# Remove quotes and save back
with open('Data/ProBowlers.csv', 'w') as file:
    for line in lines:
        file.write(line.strip('"\n') + '\n')