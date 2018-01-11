cmake_minimum_required(VERSION 3.5)
project(DepGraph)

find_package(Threads REQUIRED)

include(FindProtobuf)
find_package(Protobuf REQUIRED)

find_package( Boost 1.6 COMPONENTS program_options REQUIRED )

include_directories(${PROTOBUF_INCLUDE_DIR})
include_directories(${Boost_INCLUDE_DIRS})
include_directories(SYSTEM)
include_directories(${CMAKE_BINARY_DIR})

add_custom_command(
    OUTPUT
    ${CMAKE_BINARY_DIR}/inst_dep_record.pb.cc
    ${CMAKE_BINARY_DIR}/inst_dep_record.pb.h
    ${CMAKE_BINARY_DIR}/inst_dep_record_pb2.py
    DEPENDS
    $ENV{gem5_root}/src/proto/inst_dep_record.proto
    COMMAND
        protoc -I=$ENV{gem5_root}/src/proto --cpp_out=${CMAKE_BINARY_DIR}
            $ENV{gem5_root}/src/proto/inst_dep_record.proto
    COMMAND
        protoc -I=$ENV{gem5_root}/src/proto --python_out=${CMAKE_BINARY_DIR}
            $ENV{gem5_root}/src/proto/inst_dep_record.proto
    VERBATIM
    )

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -O3")
set(GRAPH_SOURCE_FILES
    main.cc
    log.cc
    protoio.cc
    ${CMAKE_BINARY_DIR}/inst_dep_record.pb.cc dep_count.cc dep_count.hh dep_count.hh)
add_executable(graph ${GRAPH_SOURCE_FILES})
TARGET_LINK_LIBRARIES(graph LINK_PUBLIC
    ${PROTOBUF_LIBRARY} ${Boost_LIBRARIES})
