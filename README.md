# Revisiting TCP CCA
Study of Fairness and throughput for TCP Reno, CUBIC and BBR in high scale network.

---

## Finding 1

> The Mathis model for TCP NewReno throughput is valid at CoreScale only if the congestion event rate (p) and model parameter C are calculated using the CWND-halving rate, rather than the conventional packet loss rate that is typically used for EdgeScale.

### To validate this finding on CloudLab:

* Open the [CloudLab profile](https://www.cloudlab.us/p/nyunetworks/imc-revisiting). Leave parameters at their default settings, and reserve resources at CloudLab Utah. Wait for resources to come up and for startup scripts to be complete. Open an SSH terminal at the router.
* On the router: run `bash /local/repository/cloudlab-scripts/validate.sh` and confirm that you see about 24-25 Gbps sum throughput for multiple flows (on average 2.5 Gbps for each of the 10 flows), 8-10 Gbps throughput for single flow, and 0-1 ms RTT.
* On the router: run `bash /local/repository/cloudlab-scripts/setup-core.sh` and confirm that you see about **10 Gbps** sum throughput for multiple flows (on average 1 Gbps for each of the 10 flows), 7-10 Gbps throughput for single flow, and 0-2 ms RTT.
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 10 1800 reno 10 0.01` to generate 1000 flows with 20ms delay. To change the number of flows to 3000 and 5000, change the 7th parameter from 10 to 30 and 50 respectively. Three files are generated-
  1. 'packet_loss_iperf.csv' which has the mean rtt, bandwidth, number of retransmits, number of congestion window halving events, packet loss rate and congestion window halving rate for each flow.

     Example output file from running the command is [packet_loss_iperf.csv](https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/blob/main/cloudlab-outputs/packet_loss_iperf_core_1000.csv)
  2. 'output_mathis_C_iperf.csv' has the total bandwidth, total number of retransmits, total congestion window halving events, 'C' value using packet loss rate, 'C' value using congestion window halving rate, ratio of packets dropped at the router to congestion window halving event.

     Example output from running the command is [output_mathis_C_iperf.csv](https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/blob/main/cloudlab-outputs/output_mathis_C_iperf.csv)
     `time_interval,time_duration,ports,sum(y_values),total_cwnd_half,total_retransmission,total_retransmission/total_cwnd_half,np.nanmean(list_ratio),reg_simple1.intercept_,reg_simple1.coef_[0],reg_simple2.intercept_,reg_simple2.coef_[0],router_dropped,router_sent,router_dropped/total_cwnd_half
0.01,1800,1000,10045527000,328005,150056,0.457480831084892,0.4592942121018375,0.0,2.6682251202316913,0.0,3.985303969272882,98829,1686597751,0.30130333379064345`
  4. 'linear_reg_plot.pdf' contains two plots showing
     
     a. x=mss/rtt\*sqrt(packet loss rate) vs actual bandwidth per flow; regression line and x=mss/rtt\*sqrt(packet loss rate) vs predicted bandwidth per flow.
     
     b. x=mss/rtt\*sqrt(cwnd halving rate) vs actual bandwidth per flow; linear regression line and x=mss/rtt\*sqrt(cwnd halving rate) vs predicted bandwidth per flow.
     
    Example output from running the command is [linear_reg_plot_core_1000.pdf](https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/blob/main/cloudlab-outputs/linear_reg_plot_core_1000.pdf) 

* On the router: run `bash /local/repository/cloudlab-scripts/setup-edge.sh` and confirm that you see about **100 Mbps** sum throughput for multiple flows (on average 10 Mbps for each of the 10 flows), 100 Mbps throughput for single flow, and 0-2 ms RTT.
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 1 1800 reno 1 0.01` to to generate 10 flows with 20ms delay. To change the number of flows to 30 and 50, change the 7th parameter from 1 to 3 and 5 respectively. Three files are generated-
  1. 'packet_loss_iperf.csv' which has the mean rtt, bandwidth, number of retransmits, number of congestion window halving events, packet loss rate and congestion window halving rate for each flow.

     Example output file can from running the command is 'packet_loss_iperf_edge_10.csv'
  2. 'output_mathis_C_iperf.csv' has the total bandwidth, total number of retransmits, total congestion window halving events, 'C' value using packet loss rate, 'C' value using congestion window halving rate, ratio of packets dropped at the router to congestion window halving event.

     Example output from running the command is [output_mathis_C_iperf.csv](https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/blob/main/cloudlab-outputs/output_mathis_C_iperf.csv)
     
  4. 'linear_reg_plot.pdf' contains two plots showing
     
     a. x=mss/rtt\*sqrt(packet loss rate) vs actual bandwidth per flow; regression line and x=mss/rtt\*sqrt(packet loss rate) vs predicted bandwidth per flow.
  
     b. x=mss/rtt\*sqrt(cwnd halving rate) vs actual bandwidth per flow; linear regression line and x=mss/rtt\*sqrt(cwnd halving rate) vs predicted bandwidth per flow.

      Example output from running the command is linear_reg_plot_edge_10.pdf

### To validate this finding on FABRIC:

* In the Jupyter environment, select File > New > Terminal and in this terminal, run `https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP`
* Open fabric-notebook subdirectory inside IMC directory.
* Run the notebook `00-reserve.ipynb` to reserve the resources. This will reserve 10 sender-reciver pair and a router. All the required dependencies or modules will be installed.
  
Example notebook
* Run the notebook `01-validate.ipynb' and confirm that you see about 24-25 Gbps sum throughput for multiple flows (on average 2.5 Gbps for each of the 10 flows), 8-10 Gbps throughput for single flow, and 0-1 ms RTT.

Example notebook
* Run the notebook `02-setup-core.ipynb` and confirm that you see about **10 Gbps** sum throughput for multiple flows (on average 1 Gbps for each of the 10 flows), 7-10 Gbps throughput for single flow, and 0-2 ms RTT.
  
Example notebook

* Run the notebook `generate-flows-one-cca.ipynb`. Set the parameters as mentioned in the notebook to run experiments with reno at 20ms delay.
  
Example notebook

* Run the notebook `04-setup-edge.ipynb` and confirm that you see about **100 Mbps** sum throughput for multiple flows (on average 10 Mbps for each of the 10 flows), 100 Mbps throughput for single flow, and 0-2 ms RTT.
  
Example notebook
* Run the notebook `generate-flows-one-cca.ipynb`. Vary the parameters as mentioned in the notebook to run experiments with reno at 20ms delay.

Example notebook

Discussion:

TBD

## Finding 2

> NewReno and Cubic show high intra-CCA fairness in CoreScale, in line with past research. BBR shows poor intra-CCA fairness in CoreScale, contradicting previous research in the edge setting.

To validate this finding on CloudLab:

* Open the [CloudLab profile](https://www.cloudlab.us/p/nyunetworks/imc-revisiting). Leave parameters at their default settings, and reserve resources at CloudLab Utah. Wait for resources to come up and for startup scripts to be complete. Open an SSH terminal at the router.
* On the router: run `bash /local/repository/cloudlab-scripts/validate.sh` and confirm that you see about 24-25 Gbps sum throughput for multiple flows (on average 2.5 Gbps for each of the 10 flows), 8-10 Gbps throughput for single flow, and 0-1 ms RTT.
* On the router: run `bash /local/repository/cloudlab-scripts/setup-core.sh` and confirm that you see about **10 Gbps** sum throughput for multiple flows (on average 1 Gbps for each of the 10 flows), 7-10 Gbps throughput for single flow, and 0-2 ms RTT.
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 10 1800 reno 10 1`.
  'jfi.csv' file is created (if there is none otherwise append the current result in new line). It has cca, duration of expt(sec), base RTT(ms)', total bandwidth(Kbps), sum of square of bandwidth, flow count and JFI.
  Example output from running the command is [JFI.csv](https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/blob/main/cloudlab-outputs/jfi.csv)
  `CCA,Duration of Expt(sec),Base RTT(ms),Total Bandwidth(Kbps),Sum of sq of BW,Flow Count,JFI
  reno,1800,20,10045527,102111493807,1000,0.9882590974377773`
  
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 10 1800 cubic 10 1`.
  
  Example output from running the command is ''
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 10 1800 bbr 10 1`.
  
  Example output from running the command is ''
* On the router: run `bash /local/repository/cloudlab-scripts/setup-edge.sh` and confirm that you see about **100 Mbps** sum throughput for multiple flows (on average 10 Mbps for each of the 10 flows), 100 Mbps throughput for single flow, and 0-2 ms RTT.
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 1 1800 reno 1 1`.
  Example output from running the command is ''
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 1 1800 cubic 1 1`.
  Example output from running the command is ''
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 1 1800 bbr 1 1`.
  Example output from running the command is ''

To validate this finding on FABRIC:

* In the Jupyter environment, select File > New > Terminal and in this terminal, run `https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP`
* Open fabric-notebook subdirectory inside IMC directory.
* Run the notebook `00-reserve.ipynb` to reserve the resources. This will reserve 10 sender-reciver pair and a router. All the required dependencies or modules will be installed.
  
Example notebook
* Run the notebook `01-validate.ipynb' and confirm that you see about 24-25 Gbps sum throughput for multiple flows (on average 2.5 Gbps for each of the 10 flows), 8-10 Gbps throughput for single flow, and 0-1 ms RTT.

Example notebook
* Run the notebook `02-setup-core.ipynb` and confirm that you see about **10 Gbps** sum throughput for multiple flows (on average 1 Gbps for each of the 10 flows), 7-10 Gbps throughput for single flow, and 0-2 ms RTT.
  
Example notebook
* Run the notebook `generate-flows-one-cca.ipynb`. Vary the parameters as mentioned in the notebook to run experiments with reno, bbr and cubic.

Example notebook
* Run the notebook `04-setup-edge.ipynb` and confirm that you see about **100 Mbps** sum throughput for multiple flows (on average 10 Mbps for each of the 10 flows), 100 Mbps throughput for single flow, and 0-2 ms RTT.
  
Example notebook
* Run the notebook `generate-flows-one-cca.ipynb`. Vary the parameters as mentioned in the notebook to run experiments with reno, bbr and cubic.

Example notebook
  

  
Discussion: 

TBD

## Finding 3

> Cubic achieves 70 to 80% of total throughput when competing with an equal number of NewReno flows at CoreScale, while BBR is highly unfair to loss-based CCA, i.e., NewReno and Cubic. These results are in line with past research in the edge setting.

To validate this finding on CloudLab:

TBD

To validate this finding on FABRIC:

TBD

Discussion: 

TBD

## Extension to intermediate settings
