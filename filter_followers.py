import csv

# Open the CSV file
with open('followers_insta.csv', 'r') as file:
    reader = csv.DictReader(file)
    usernames = set()
    
    # Collect unique usernames
    for row in reader:
        username = row['username']
        if username not in usernames:
            usernames.add(username)

# Save the unique usernames back to the CSV file
with open('followers_insta.csv', 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=['username'])
    writer.writeheader()
    
    for username in usernames:
        writer.writerow({'username': username})

print("Duplicates removed and file saved successfully!")

