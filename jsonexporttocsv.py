import requests
import csv
import json

# job_event data
url = "http://m_buck:b7SqUA4yB7qf@ansible.localnet/api/v2/jobs/"
job = input('Enter Job ID: ')
end = "/job_events/"
stdout = "/stdout/"


def result(var):
    r = requests.get(url + job + end)
    data = r.json()
    res = data['results'][(var)]['event_data']['res']['stdout_lines']
    return res


def stdoutres(var1):
    r = requests.get(url + job + stdout)
    data1 = r.json()
    return data1

# print(result(3))
# print(result(5))
# print(result(7))
# print(result(9))

print("Creating .csv file for job " + job)

# csvjob = 'Job' + job + '.csv'
textjob = 'Job' + job + '.txt'

# with open(csvjob, 'w', newline='') as f:
#     writer = csv.writer(f, delimiter=',')
#     writer.writeheader()
#     writer.writerow(result(3))
#     writer.writerow(result(5))
#     writer.writerow(result(7))
#     writer.writerow(result(9))

with open(textjob, 'w', newline='') as f:
    json.dump(result(3), f)
    json.dump(result(5), f)
    json.dump(result(7), f)
    json.dump(result(9), f)
