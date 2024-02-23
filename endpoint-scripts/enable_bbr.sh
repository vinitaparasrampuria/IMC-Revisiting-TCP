sudo apt update
sudo apt install -y --install-recommends linux-generic-hwe-16.04
sudo echo "tcp_bbr" >> /etc/modules-load.d/modules.conf
sudo echo "net.core.default_qdisc=fq" >> /etc/sysctl.conf
sudo echo "net.ipv4.tcp_congestion_control=bbr" >> /etc/sysctl.conf
sudo sysctl -p
sudo sysctl net.ipv4.tcp_available_congestion_control
sudo sysctl net.ipv4.tcp_congestion_control
sudo lsmod | grep bbr
