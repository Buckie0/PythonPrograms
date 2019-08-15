from datetime import datetime
import csv


def main():
    start_time = datetime.now()

    with open('devices.csv', encoding="utf-8") as devices:
        reader = csv.DictReader(devices)
        next(reader)  # skips the header

        f = open("hosts.yaml", "w+")

        for row in reader:
            net_name_orig1 = (row['Network Name'])
            ip_addr = (row['Management IP'])
            net_name_edited = net_name_orig1.replace('-', '_')
            net_name = net_name_edited.replace('.', '_')

            f.write(net_name + ':\n')
            f.write(f"    hostname: {ip_addr}\n")
            f.write("    groups:\n")
            f.write(f"        - cisco-ios\n")

        f.close()

    print("\nElapsed time: " + str(datetime.now() - start_time))


main()
