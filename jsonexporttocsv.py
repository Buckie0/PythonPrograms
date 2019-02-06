import requests
import csv
import json
# from nested_lookup import nested_lookup

url = "http://m_buck:b7SqUA4yB7qf@ansible.localnet/api/v2/jobs/"
job = input('Enter Job ID: ')
end = "/job_events/?page="
page = 0

print('Getting Data...')

textjob = 'Job' + job + '.json'
csvjob = 'Job' + job + '.csv'

while True:
    page += 1
    r = requests.get(url + job + end + str(page))
    data = r.json()
    response = r.status_code
    print("Page " + str(page))
    with open(textjob, 'w') as b:
        json_data = json.dumps(data)

    if response != 200:
        print("Finshed")
        b.close()
        break

with open(textjob) as f:
    newdata = json.loads(f)


print(type(newdata))

# with open(csvjob, 'a', newline='\n') as f:
#     writer = csv.writer(f)
#     writer.writerow(hosts)

# with open(textjob) as f:
#     newdata = json.loads(f)
# print(newdata)

# list = newdata["results"]

# print(list)


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



# print('Creating .txt file for job ' + job)
# with open(csvjob, 'a', newline='\n') as c:
#     writer = csv.writer(c)
#     writer.writerows(find('stdout_lines', list))
