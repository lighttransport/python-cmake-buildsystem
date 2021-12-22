rmdir /s /q build
mkdir build

cd build
cmake.exe -G "Visual Studio 16 2019" -A x64 ..
