FROM 763104351884.dkr.ecr.ap-northeast-1.amazonaws.com/tensorflow-training:2.4-gpu-py37

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get -y update && \ 
    apt-get -y upgrade && \
    apt-get -y install wget cmake build-essential libopenmpi-dev software-properties-common --no-install-recommends nvidia-utils-460 && \
    rm -rf /var/lib/apt/lists/* && \
    python -m pip install numpy pandas && \
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
