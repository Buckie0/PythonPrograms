ip_addr = input("Please enter an IP: ")
octets = ip_addr.split(".")

print()
print("{:^15}{:^15}{:^15}{:^15}".format("Octet1", "Octet2",
                                        "Octet3", "Octet4"))
print("-" * 60)
print("{:^15}{:^15}{:^15}{:^15}".format(*octets))
print("{:^15}{:^15}{:^15}{:^15}".format(bin(int(octets[0])),
                                        bin(int(octets[1])),
                                        bin(int(octets[2])),
                                        bin(int(octets[3]))))
print("{:^15}{:^15}{:^15}{:^15}".format(hex(int(octets[0])),
                                        hex(int(octets[1])),
                                        hex(int(octets[2])),
                                        hex(int(octets[3]))))
print("-" * 60)
print()
