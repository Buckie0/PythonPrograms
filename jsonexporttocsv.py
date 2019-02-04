import requests
import csv
import json
from nested_lookup import nested_lookup

# job_event data
url = "http://m_buck:b7SqUA4yB7qf@ansible.localnet/api/v2/jobs/"
job = input('Enter Job ID: ')
end = "/job_events/?page="
page = 0

print("Creating .txt file for job " + job)

csvjob = 'Job' + job + '.csv'
textjob = 'Job' + job + '.txt'

while True:
    page += 1
    r = requests.get(url + job + end + str(page))
    data = r.json()
    result1 = nested_lookup("stdout_lines", data)
    response = r.status_code
    if response == "200":
        page += 1
        print("Page " + str(page))
        with open(textjob, 'a') as f:
            out = json.dump(result1, f, indent=1)
        continue
    elif response != "200":
        break


# Testing

r = requests.get(url + job + end + str(page))
data = r.json()
result1 = nested_lookup("stdout_lines", data)
response = r.status_code

for x in result1:
    if response == "200":
        page += 1
        print("Page " + str(page))
        with open(csvjob, 'w') as f:
            fields = ["Device Name", "Command"]
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            writer.writerows(result1)
