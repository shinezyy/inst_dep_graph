#include <iostream>
#include <boost/program_options.hpp>

#include "protoio.hh"
#include "log.hh"

namespace po = boost::program_options;
using namespace std;

int main(int argc, const char *argv[]) {

    po::options_description desc("Allowed options");
    desc.add_options()
        ("help,h", "print help")
        ("input,i", po::value<string>(), "input gziped proto file")
        ;
    po::variables_map vm;
    po::store(po::parse_command_line(argc, argv, desc), vm);
    po::notify(vm);

    if (vm.count("help")) {
        cout << desc << "\n";
        return 1;
    }
    if (vm.count("input")) {
        cout << "input file:" << vm["input"].as<string>() << endl;
    } else {
        panic("No input file given!");
    }

    ProtoInputStream trace(vm["input"].as<string>());

    return 0;
}
