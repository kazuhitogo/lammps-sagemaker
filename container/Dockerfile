FROM nvidia/cuda:11.4.2-devel-ubuntu20.04
# FROM 763104351884.dkr.ecr.ap-northeast-1.amazonaws.com/tensorflow-training:2.6.0-gpu-py38-cu112-ubuntu20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get -y update && \ 
    apt-get -y upgrade && \
    apt-get -y install python3.9 python3-pip wget cmake && \
#     apt-get -y install build-essential libopenmpi-dev software-properties-common nvidia-utils-460 && \
    apt-get -y install build-essential libopenmpi-dev software-properties-common && \
    pip install numpy pandas && \
    ln -s /usr/bin/python3.9 /usr/bin/python && \
    mkdir -p /program/lammps201029 && \
    cd /program/lammps201029 && \
    wget https://download.lammps.org/tars/lammps-29Oct2020.tar.gz && \
    tar zxvf lammps-29Oct2020.tar.gz && \
    mkdir -p /program/lammps201029/build && \
    cd /program/lammps201029/build && \
    cmake /program/lammps201029/lammps-29Oct20/cmake \
          -DCMAKE_INSTALL_PREFIX="~/program/lammps201029/lammps-29Oct20" \
          -DPKG_GPU=yes \
          -DPKG_MOLECULE=yes \
          -DPKG_BODY=yes \
          -DPKG_KSPACE=yes \
          -DPKG_RIGID=yes \
          -DPKG_REPLICA=yes \
          -DGPU_API=cuda \
          -DGPU_PREC=mixed \
          -DGPU_ARCH="sm_72" \
          -DBUILD_MPI=yes \
          -DBUILD_OMP=yes \
          -DPKG_MISC=yes && \
    make -j 4 && \
    make install
    
    
    
#     apt-get install -y build-essential libopenmpi-dev software-properties-common nvidia-utils-460
# RUN add-apt-repository ppa:gladky-anton/lammps -y && \
#     add-apt-repository ppa:openkim/latest -y && \
#     apt-get -y install lammps-stable lammps-stable-doc lammps-stable-data openkim-models && \
#     git clone git://github.com/lammps/lammps.git && \
#     mkdir /lammps/build 
    
# WORKDIR /lammps/build
# RUN cmake -D BUILD_MPI=yes -D PKG_GPU=on  -D GPU_API=cuda -D GPU_ARCH=sm_80 -DCMAKE_LIBRARY_PATH=/usr/local/cuda/lib64/stubs ../cmake && \
#     make -j 4 && \
#     make install && \
#     ln -s /lammps/build/lmp /usr/bin/

# ENTRYPOINT ["bash"]
