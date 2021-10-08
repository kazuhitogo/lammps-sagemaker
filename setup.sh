#!/bin/bash

distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
sudo curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.repo | sudo tee /etc/yum.repos.d/nvidia-docker.repo
sudo yum install -y nvidia-docker2

mkdir -p /home/ec2-user/SageMaker/docker/
sudo mv /lib/systemd/system/docker.service /lib/systemd/system/docker.service.org
sudo cp ./docker.service /lib/systemd/system/
sudo systemctl daemon-reload
sudo systemctl restart docker

