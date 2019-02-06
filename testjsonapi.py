import requests
import csv
import json
# from nested_lookup import nested_lookup

url = "https://swapi.co/api/"
# job = input('Enter Job ID: ')
end = "people/?page="
page = 0

csvjob = 'Job' + '.csv'

# def PullDataCSV():
#     page = 1
#     print("Page " + str(page))
#     result1 = nested_lookup('name', data)
#     homeworld = nested_lookup('homeworld', data)
#     page += 1
#     with open(csvjob, 'w') as f:
#         # fields = ["Name", "Link to Homeworld"]
#         # writer = csv.DictWriter(f, fieldnames=fields)
#         writer = csv.writer(f)
#         # writer.writeheader()
#         writer.writerows(result1)
#         writer.writerows(homeworld)

print('Getting Data...')
while True:
    page += 1
    print("Page " + str(page))
    r = requests.get(url + end + str(page))
    data = r.json()
#     result1 = nested_lookup('name', data)
#     homeworld = nested_lookup('homeworld', data)
    response = r.status_code
    textjob = 'Job' + '.json'
    with open(textjob, 'a') as f:
        out = json.dump(data, f, indent=1)
    if response != 200:
        break
        f.close()
        print("Creating file")

with open(textjob) as f:
    string = json.loads(f)

