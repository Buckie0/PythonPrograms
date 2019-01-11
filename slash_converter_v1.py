from netaddr import *
import re

input_file = open('subnets.txt', 'r', encoding='utf-8').read()

input_file_split = re.findall("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\/\d{1,2}", input_file)

#print(input_file_split)
cidr_list = []
for x in input_file_split:
    cidr_list.append((IPNetwork(x).cidr))

#print(cidr_list)

cidr_list_post = re.findall("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\/\d{1,2}", str(cidr_list))
#print(cidr_list_post)

for v in cidr_list_post:
    #print(IPNetwork(v).network)
    #print(IPNetwork(v).netmask)
    print((IPNetwork(v).network), (IPNetwork(v).netmask))
