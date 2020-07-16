cmake_minimum_required(VERSION 2.8.12)
project(test_package CXX)

find_package(quazip REQUIRED)

add_executable(${PROJECT_NAME} example.cpp)

target_link_libraries(${PROJECT_NAME} quazip)
