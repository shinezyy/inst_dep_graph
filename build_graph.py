#!/usr/bin/env python3.6


# The ASCII trace format uses one line per instruction with the format
# instruction sequence number, (optional) pc, (optional) weight, type
# (optional) flags, (optional) phys addr, (optional) size, comp delay,
# (repeated) order dependencies comma-separated, and (repeated) register
# dependencies comma-separated.
#
# examples:
# seq_num,[pc],[weight,]type,[p_addr,size,flags,]comp_delay:[rob_dep]:
# [reg_dep]
# 1,35652,1,COMP,8500::
# 2,35656,1,COMP,0:,1:
# 3,35660,1,LOAD,1748752,4,74,500:,2:
# 4,35660,1,COMP,0:,3:
# 5,35664,1,COMP,3000::,4
# 6,35666,1,STORE,1748752,4,74,1000:,3:,4,5
# 7,35666,1,COMP,3000::,4
# 8,35670,1,STORE,1748748,4,74,0:,6,3:,7
# 9,35670,1,COMP,500::,7

import protolib
import sys
import os
from os.path import join as pjoin

# Import the packet proto definitions. If they are not found, attempt
# to generate them automatically. This assumes that the script is
# executed from the gem5 root.
try:
    import inst_dep_record_pb2
except:
    print("Did not find proto definition, attempting to generate")
    from subprocess import call
    gem5_root = os.environ['gem5_root']
    error = call(['protoc', '--python_out={}'.format(os.getcwd()),
        '--proto_path={}'.format(pjoin(gem5_root, 'src/proto')),
        pjoin(gem5_root, 'src/proto/inst_dep_record.proto')])
    if not error:
        import inst_dep_record_pb2
        print("Generated proto definitions for instruction dependency record")
    else:
        print("Failed to import proto definitions")
        exit(-1)

def main():
    if len(sys.argv) != 2:
        print("Usage: ", sys.argv[0], " <protobuf input>")
        exit(-1)

    # Open the file on read mode
    proto_in = protolib.openFileRd(sys.argv[1])

    # Read the magic number in 4-byte Little Endian
    magic_number = proto_in.read(4)

    if magic_number != b'gem5':
        print("Unrecognized file")
        exit(-1)

    print("Parsing packet header")

    # Add the packet header
    header = inst_dep_record_pb2.InstDepRecordHeader()
    protolib.decodeMessage(proto_in, header)

    print("Object id:", header.obj_id)
    print("Tick frequency:", header.tick_freq)

    print("Parsing packets")

    num_packets = 0
    num_regdeps = 0
    num_dep = [0]*320000000
    packet = inst_dep_record_pb2.InstDepRecord()

    # Decode the packet messages until we hit the end of the file
    while protolib.decodeMessage(proto_in, packet):
        num_packets += 1
        # Write to file the repeated field register dependency
        if num_packets % 10**7 == 0:
            print(num_packets)
        if packet.reg_dep:
            num_regdeps += 1 # No. of packets with atleast 1 register dependency
            for dep in packet.reg_dep:
                inst_seq = int(dep)
                num_dep[inst_seq] += 1

    print("Parsed packets:", num_packets)
    print("Packets with at least 1 reg dep:", num_regdeps)
    proto_in.close()

    print('Counting dependancies')
    dep_map = {}
    for n in num_dep:
        if n in dep_map:
            dep_map[n] += 1
        else:
            dep_map[n] = 1

    print(dep_map)


if __name__ == "__main__":
    main()
