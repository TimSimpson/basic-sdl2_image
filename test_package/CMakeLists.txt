cmake_minimum_required(VERSION 3.5)
project(test_package)

set(CMAKE_CXX_STANDARD 17)

find_package(SDL2)
if(TARGET SDL2::SDL2-static)
    set(SDL2_TARGET SDL2::SDL2-static)
elseif(TARGET SDL2::SDL2)
    set(SDL2_TARGET SDL2::SDL2)
endif()

find_package(sdl2_image)


add_executable(Sdl2ImageSimple WIN32 ${CMAKE_CURRENT_SOURCE_DIR}/Sdl2ImageSimple.cpp)
target_link_libraries(Sdl2ImageSimple PUBLIC "${SDL2_TARGET}" sdl2_image::sdl2_image)
