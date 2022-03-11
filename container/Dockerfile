FROM 763104351884.dkr.ecr.us-east-2.amazonaws.com/tensorflow-training:1.15.0-gpu-py3
ENV DEBIAN_FRONTEND=noninteractive

RUN mkdir /workspace && \
    apt-get -y update && \
    apt install nvidia-utils-410 cmake -y && \
    mkdir -p /program/lammps201029 && \
    cd /program/lammps201029 && \
    wget https://download.lammps.org/tars/lammps-29Oct2020.tar.gz && \
    tar zxvf lammps-29Oct2020.tar.gz && \
    mkdir -p /program/lammps201029/build && \
    cd /program/lammps201029/build && \
    cmake /program/lammps201029/lammps-29Oct20/cmake \
        -DCMAKE_INSTALL_PREFIX="../" \
        -DCUDA_TOOLKIT_ROOT_DIR=/usr/local/cuda \
        -DPKG_MOLECULE=yes \
        -DPKG_BODY=yes \
        -DPKG_KSPACE=yes \
        -DPKG_RIGID=yes \
        -DPKG_REPLICA=yes \
        -DPKG_MISC=yes \
        -DPKG_GPU=yes \
        -DGPU_API=cuda \
        -DGPU_PREC=mixed \
        -DGPU_ARCH=sm_75 \
        -DBUILD_MPI=yes \
        -DBUILD_OMP=yes  && \
    make -j 4 && \
    make install
