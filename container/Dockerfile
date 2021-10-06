FROM 763104351884.dkr.ecr.ap-northeast-1.amazonaws.com/tensorflow-training:2.6.0-gpu-py38-cu112-ubuntu20.04

RUN apt-get -y update && \ 
    apt-get -y upgrade && \
    apt-get install -y build-essential libopenmpi-dev software-properties-common nvidia-utils-460
RUN add-apt-repository ppa:gladky-anton/lammps -y && \
    add-apt-repository ppa:openkim/latest -y && \
    apt-get -y install lammps-stable lammps-stable-doc lammps-stable-data openkim-models && \
    git clone git://github.com/lammps/lammps.git && \
    mkdir /lammps/build 
    
WORKDIR /lammps/build
RUN cmake -D BUILD_MPI=yes -D PKG_GPU=on  -D GPU_API=cuda -D GPU_ARCH=sm_75 -DCMAKE_LIBRARY_PATH=/usr/local/cuda/lib64/stubs ../cmake && \
    make -j 4 && \
    make install && \
    ln -s /lammps/build/lmp /usr/bin/

# ENTRYPOINT ["bash"]