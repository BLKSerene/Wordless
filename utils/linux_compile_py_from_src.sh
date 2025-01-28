#!/bin/bash
# ----------------------------------------------------------------------
# Utilities: Linux - Compile Python from source
# Copyright (C) 2018-2025  Ye Lei (叶磊)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
# ----------------------------------------------------------------------

# Install build dependencies for Python
# Reference: https://devguide.python.org/getting-started/setup-building/#linux
if ! grep -Fxq "deb-src http://cn.archive.ubuntu.com/ubuntu/ bionic main" "/etc/apt/sources.list"; then
    sudo sh -c "echo 'deb-src http://cn.archive.ubuntu.com/ubuntu/ bionic main' >> /etc/apt/sources.list"
fi

sudo apt-get update
sudo apt-get -y build-dep python3
sudo apt-get -y install build-essential gdb lcov pkg-config libbz2-dev libffi-dev libgdbm-dev libgdbm-compat-dev liblzma-dev libncurses5-dev libreadline6-dev libsqlite3-dev libssl-dev lzma lzma-dev tk-dev uuid-dev zlib1g-dev

# Compile Python from source
PY_VER=3.11.9
PY_PACKAGE="Python-$PY_VER.tgz"
PY_FOLDER="Python-$PY_VER"

if [ ! -d $PY_FOLDER ]; then
    if [ ! -f $PY_PACKAGE ]; then
        wget "https://www.python.org/ftp/python/$PY_VER/$PY_PACKAGE"
    fi

    tar -xf $PY_PACKAGE
fi

cd $PY_FOLDER
# PyInstaller requires "--enable-shared"
./configure --enable-optimizations --with-lto --enable-shared
make -s -j
sudo make altinstall
cd ..

# Fix error while loading shared libraries
sudo ldconfig

# Install 3rd-party libraries
python3.11 -m pip install --upgrade pip setuptools
pip3.11 install -r requirements_dev.txt
pip3.11 cache purge

# Fix libxcb-xinerama.so
sudo apt-get install libxcb-xinerama0

# Clean files
sudo rm $PY_PACKAGE
sudo rm -r $PY_FOLDER

sudo apt-get -y autoremove
sudo apt-get clean
