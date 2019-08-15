from napalm import get_network_driver


driver = get_network_driver('eos')
with driver('localhost', 'vagrant', 'vagrant', optional_args={'port': 12443}) as device:
    facts = (device.get_facts())

print("Gathering Device Information...")

for i in facts:
    if type(facts[i]) == list:
        for k in facts[i]:
            print("\t -{}".format(k))
    else:
        print("{}: {}".format(i, facts[i]))
