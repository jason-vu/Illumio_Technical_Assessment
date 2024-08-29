"""
Write a program that can parse a file containing flow log data and maps each row to a tag based on a lookup table.
The lookup table is defined as a csv file, and it has 3 columns, dstport,protocol,tag.
The dstport and protocol combination decide what tag can be applied. 

The program should generate an output file containing the following: 
    Count of matches for each tag, sample o/p shown below
    Count of matches for each port/protocol combination
"""
import csv

# insert additional protocol numbers as necessary
# string protocol number -> protocol
protocol_map = {
    "1": "icmp",
    "6": "tcp",
    "17": "udp"
}


logs = open("flow_logs.txt")

split_logs = []
for log in logs:
    split_logs.append(log.split(' '))

# dstport is field 6
# protocol is field 7


# process lookup table
# (dstport, protocol) tuple -> tag
lookup_table = {}
with open("lookup_table.csv", mode="r") as file:
    csvFile = csv.reader(file)
    for line in csvFile:
        dstport = line[0]
        protocol = line[1]
        tag = line[2]

        lookup_table[(dstport, protocol)] = tag


tag_counts = {}
port_protocol_counts = {}

# Count of matches for each tag
for splitted_log in split_logs:
    dstport = splitted_log[6]
    protocol = protocol_map[splitted_log[7]]

    port_protocol_counts[(dstport, protocol)] = port_protocol_counts.get((dstport, protocol), 0) + 1

    if (dstport, protocol) in lookup_table:
        tag = lookup_table[(dstport, protocol)]

        tag_counts[tag] = tag_counts.get(tag, 0) + 1
    else:
        tag_counts["Untagged"] = tag_counts.get("Untagged", 0) + 1


# write output
output = open("output.txt", "w")
output.write("Tag Counts:\nTag,Count\n")
for key, val in tag_counts.items():
    output.write(str(key) + ',' + str(val) + '\n')

output.write("Port/Protocol Combination Counts:\nPort,Protocol,Count\n")
for key, val in port_protocol_counts.items():
    output.write(str(key[0]) + ',' + str(key[1]) + ',' + str(val) + '\n')