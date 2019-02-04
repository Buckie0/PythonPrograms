import requests
import csv
import json
from nested_lookup import nested_lookup

url = "https://swapi.co/api"
# job = input('Enter Job ID: ')
end = "people/"
page = 0

print("Creating .csv file")

csvjob = 'Job' + '.csv'

r = requests.get(url + end + str(page))
data = r.json()
result1 = nested_lookup('name', data)
homeworld = nested_lookup('homeworld', data)
response = r.status_code

while True:
    page += 1
    print("Page " + str(page))
    with open(csvjob, 'w') as f:
        fields = ["Device Name", "Command"]
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(result1)
        writer.writerows(homeworld)
        if response != "200":
            continue
        else:
            print("Finshed")
# textjob = 'Job' + '.txt'

# while True:
#     r = requests.get(url + end + str(page))
#     data = r.json()
#     result1 = nested_lookup("stdout_lines", data)
#     response = r.status_code
#     page += 1
#     print("Page " + str(page))
#     with open(textjob, 'a') as f:
#         out = json.dump(result1, f, indent=1)
#     if response != "200":
#         continue
#     else:
#         print("Finshed")


# Testing
