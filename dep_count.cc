//
// Created by zyy on 1/11/18.
//
#include <map>
#include <array>
#include <iostream>
#include <cinttypes>
#include <ctime>


#include "protoio.hh"
#include "inst_dep_record.pb.h"


using namespace std;

array<uint32_t, 400'000'000> counts;


void countDependancy(ProtoInputStream &trace) {
    ProtoMessage::InstDepRecord inst;
    ProtoMessage::InstDepRecordHeader dep_header;

    trace.read(dep_header);
    cout << "skip header!\n";

    uint64_t num_msg = 0;
    clock_t start_s = clock();
    while (trace.read(inst)) {
        num_msg += 1;
        if (inst.reg_dep_size()) {
            for (auto &it: inst.reg_dep()) {
                counts[it] += 1;
            }
        }
        if (num_msg % 10'000'000 == 0) {
            cout << "*";
        }
    }
    clock_t end_s = clock();
    cout << "It takes " << (end_s - start_s)/(double(CLOCKS_PER_SEC))
        << "s to get count array of " << num_msg << " insts\n";

    start_s = clock();;
    map<uint32_t, uint32_t> dep_map;
    for (auto &it: counts) {
        if (!dep_map.count(it)) {
            dep_map[it] = 1;
        } else {
            dep_map[it] += 1;
        }
    }
    end_s = clock();
    cout << "It takes " << (end_s - start_s)/(double(CLOCKS_PER_SEC))
        << "s to get dep map\n";
}



