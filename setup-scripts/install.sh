sudo apt-get update
sudo apt-get install -y python3-pip ethtool netcat moreutils
pip3 install numpy
pip3 install pandas
pip3 install matplotlib
pip3 install seaborn
python3 -m pip install scikit-learn

csv_filename="/local/repository/cloudlab-scripts/packet_loss.csv"
with open(csv_filename, 'a', newline='') as csvfile:
  writer = csv.writer(csvfile)
  header = 'port', 'data_seg_out', 'mean_rtt', 'bandwidth_port', 'port_retrans1', 'port_retrans2', 'cwn_half_port', 'packet_loss1', 'x1', 'packet_loss2', 'x2', 'cwnd_half_rate1','x3', 'cwnd_half_rate2', 'x4', 'ratio1', 'ratio2'
  writer.writerow(header)
   
output_filename='output_mathis_C.csv'
with open(output_filename, 'a', newline='') as csvfile:
  writer = csv.writer(csvfile)
  header = 'total_ports', 'ports', 'sum(y_values)', 'total_cwnd_half', 'total_retransmission1', 'total_retransmission2', 'total_retransmission1/total_cwnd_half', 'total_retransmission2/total_cwnd_half', 'np.nanmean(list_ratio1)', 'np.nanmean(list_ratio2)', 'reg_simple1.intercept_', 'reg_simple1.coef_[0]', 'reg_simple2.intercept_', 'reg_simple2.coef_[0]', 'reg_simple3.intercept_', 'reg_simple3.coef_[0]', 'reg_simple4.intercept_', 'reg_simple4.coef_[0]', 'router_dropped', 'router_sent', 'router_dropped/total_cwnd_half'
  writer.writerow(header)
  


