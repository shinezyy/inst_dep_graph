cmake_minimum_required(VERSION 3.5)
project(SocketProtobuf)

find_package(Threads REQUIRED)

include(FindProtobuf)
find_package(Protobuf REQUIRED)

include_directories(${PROTOBUF_INCLUDE_DIR})
include_directories(${CMAKE_BINARY_DIR})
include_directories(SYSTEM)

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

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall")
set(GRAPH_SOURCE_FILES graph.cpp ${CMAKE_BINARY_DIR}/inst_dep_record.pb.cc)
add_executable(graph ${GRAPH_SOURCE_FILES})
TARGET_LINK_LIBRARIES(graph LINK_PUBLIC ${CMAKE_THREAD_LIBS_INIT}
    ${PROTOBUF_LIBRARY})
