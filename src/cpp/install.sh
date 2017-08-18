#!/bin/bash
sudo apt-get install build-essential gcc libmysql++-dev mysql-server openssl libbz2-dev libssl-dev cmake scons
sudo mysql_secure_installation
sudo mysqld --initialize

cd ~
wget https://sourceforge.net/projects/boost/files/boost/1.63.0/boost_1_63_0.tar.bz2
tar xvjf boost_1_63_0.tar.bz2
cd boost_1_63_0

./bootstrap.sh --with-toolset=gcc
sudo ./b2 toolset=gcc -j 4 install --prefix=/usr/local

echo "export BOOST_ROOT=${HOME}/boost_1_63_0" >> ~/.profile
echo "export LD_LIBRARY_PATH=${BOOST_ROOT}/stage/lib:${LD_LIBRARY_PATH}" >> ~/.profile


cd ~
git clone https://github.com/msgpack/msgpack-c.git
cd msgpack-c
git checkout cpp-1.4.2
cmake -DMSGPACK_CXX11=ON .
sudo make install



cd ~
git clone https://github.com/zaphoyd/websocketpp.git
cd websocketpp
cmake .
sudo make install


cd ~
git clone https://github.com/crossbario/autobahn-cpp.git
cd autobahn-cpp
cp -r autobahn/ /usr/local/include/


