# This script installs Mellanox QOS tools ont he router
wget https://content.mellanox.com/ofed/MLNX_OFED-23.04-0.5.3.3/MLNX_OFED_LINUX-23.04-0.5.3.3-ubuntu22.04-x86_64.tgz -P /tmp
tar -xzvf /tmp/MLNX_OFED_LINUX-23.04-0.5.3.3-ubuntu22.04-x86_64.tgz -C /tmp/
echo "deb file:/tmp/MLNX_OFED_LINUX-23.04-0.5.3.3-ubuntu22.04-x86_64/DEBS ./" | sudo tee  /etc/apt/sources.list.d/mlnx_ofed.list
wget -qO - http://www.mellanox.com/downloads/ofed/RPM-GPG-KEY-Mellanox | sudo apt-key add -
sudo chmod -R a+r  /tmp/MLNX_OFED_LINUX-23.04-0.5.3.3-ubuntu22.04-x86_64
sudo apt-get update
sudo apt install mlnx-tools mlnx-iproute2 mlnx-ethtool

