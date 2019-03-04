import requests
import csv
import json
# import pandas as pd
import os
from nested_lookup import nested_lookup

url = "http://m_buck:b7SqUA4yB7qf@ansible.localnet/api/v2/jobs/"
job = input('Enter Job ID: ')
end = "/job_events/?page="
page = 0

print('Getting Data...')

textjob = 'Job' + job + '.txt'
# textjob = os.path.dirname(os.path.abspath('Job' + job + '.json'))
csvjob = 'Job' + job + '.csv'

while True:
    page += 1
    r = requests.get(url + job + end + str(page))
    data = r.json()
    response = r.status_code
    results = data.get('results')
    print(page)
    # for i in results:
    #     host = i['name']
    #     stdout = i['stdout_lines']
    host = nested_lookup('host', results)
    stdout = nested_lookup('stdout_lines', results)
    with open(textjob, 'a',) as f:
            json.dump(host + stdout, f, indent=2)
            # json.dump(stdout, f, indent=2)
            f.write('\n')
    if response != 200:
        print("Finshed")
        f.close()
        break

# with open(textjob, 'rU') as f:
#     newdata = f.readlines()

# newdata = map(lambda x: x.rstrip(), newdata)
# newdata_json_str = "[" + ",".join(newdata) + "]"

# newdata_df = pd.read_json(newdata_json_str, lines=True)

# print(newdata_df)

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
