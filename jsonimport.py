import json
import requests
import csv

url = "http://m_buck:b7SqUA4yB7qf@ansible.localnet/api/v2/jobs/"
job = input('Enter Job ID: ')
end = "/stdout/"

# Load json date from ansible api
r = requests.get(url + job + end)
data = r.json()

# Search for required data
for result in data['results']['event_data']['res']:
    print(result['stdout'], ['stdout_lines'])

print("Creating .csv file for job " + job)

with open('Job' + job + '.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerows(result['stdout'])

# json.dumps(data, indent=4)
# result['stdout_lines']
