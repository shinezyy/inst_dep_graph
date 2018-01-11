//
// Created by zyy on 1/11/18.
//
#include <unordered_map>
#include <iostream>


#include "protoio.hh"
#include "inst_dep_record.pb.h"


using namespace std;


void countDependancy(ProtoInputStream &trace) {
    ProtoMessage::InstDepRecord inst;
    ProtoMessage::InstDepRecordHeader dep_header;

    trace.read(dep_header);
    cout << "skip header!\n";

    uint64_t num_msg = 0;
    while (trace.read(inst)) {
        num_msg += 1;
        if (inst.reg_dep_size()) {
            for (auto &it: inst.reg_dep()) {
                cout << it;
            }
            cout << "\n";
        }
        if (num_msg > 100) {
            break;
        }
    }
}



