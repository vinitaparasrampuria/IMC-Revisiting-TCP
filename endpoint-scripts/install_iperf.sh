sudo git clone https://github.com/vinitaparasrampuria/iperf.git /iperf
cd /iperf
sudo ./configure
sudo make
sudo make check
sudo make install
sudo ldconfig
cd /local/repository/cloudlab-scripts
