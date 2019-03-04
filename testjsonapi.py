import requests
import csv
import json
from nested_lookup import nested_lookup

url = 'https://swapi.co/api/'
end = 'people/?page='
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
    print('Page ' + str(page))
    r = requests.get(url + end + str(page))
    response = r.status_code
    textjob = 'Job' + '.txt'
    data = r.json()
    results = data.get('results')
    for i in results:
        name = i['name']
        height = i['height']
        homeworld = i['homeworld']
    with open(textjob, 'a',) as f:
            json.dump(name, f, indent=2)
            json.dump(height, f, indent=2)
            json.dump(homeworld, f, indent=2)
            f.write('\n')
    if response != 200:
        break
        f.close()
        print('Creating file')


# def find(key, dictionary):
#     for k, v in dictionary.items():
#         if k == key:
#             yield v
#         elif isinstance(v, dict):
#             for result in find(key, v):
#                 yield result
#         elif isinstance(v, list):
#             for d in v:
#                 for result in find(key, d):
#                     yield result

# with open(textjob) as f:
#     string = json.load(f)
#     # name = nested_lookup('name', string)
#     # homeworld = nested_lookup('homeworld', string)

# print(string)
