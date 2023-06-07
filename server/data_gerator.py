import csv
import random
from faker import Faker

# Instantiate Faker
fake = Faker()

# Define the number of rows you want in the CSV file
num_rows = 10000

# Define the field names
field_names = ["parent_page_id", "page_name", "new_page_name", "task_name", "page_description", "new_page_description",
               "task_description", "color", "status"]

# Create a CSV file and write the header row
with open("random_data.csv", "w", newline="") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=field_names)
    writer.writeheader()

    # Generate random data and write rows to the CSV file
    for _ in range(num_rows):
        data = {
            "parent_page_id": 1,
            "page_name": fake.word(),
            "new_page_name": fake.word(),
            "task_name": fake.word(),
            "page_description": fake.sentence(),
            "new_page_description": fake.sentence(),
            "task_description": fake.sentence(),
            "color": fake.color_name(),
            "status": "todo"
        }
        writer.writerow(data)

print("CSV file generated successfully.")
