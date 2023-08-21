# Revisiting TCP CCA
Study of Fairness and throughput for TCP Reno, CUBIC and BBR in high scale network.

---

## Finding 1

> The Mathis model for TCP NewReno throughput is valid at CoreScale only if the congestion event rate (p) and model parameter C are calculated using the CWND-halving rate, rather than the conventional packet loss rate that is typically used for EdgeScale.

To validate this finding on CloudLab:

* Open the [CloudLab profile](https://www.cloudlab.us/p/nyunetworks/imc-revisiting). Leave parameters at their default settings, and reserve resources at CloudLab Utah. Wait for resources to come up and for startup scripts to be complete. Open an SSH terminal at the router.
* On the router: run `bash /local/repository/cloudlab-scripts/validate.sh` and confirm that you see about 24-25 Gbps sum throughput for multiple flows (on average 2.5 Gbps for each of the 10 flows), 8-10 Gbps throughput for single flow, and 0-1 ms RTT.
* On the router: run `bash /local/repository/cloudlab-scripts/setup-core.sh` and confirm that you see about **10 Gbps** sum throughput for multiple flows (on average 1 Gbps for each of the 10 flows), 7-10 Gbps throughput for single flow, and 0-2 ms RTT.
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 10 1800 reno 10 0.01` to generate 1000 flows with 20ms delay. To change the number of flows to 3000 and 5000, change the 7th parameter from 10 to 30 and 50 respectively. Three files are generated-
  1. 'packet_loss_iperf.csv' which has the mean rtt, bandwidth, number of retransmits, number of congestion window halving events, packet loss rate and congestion window halving rate for each flow.

     Example output file from running the command is [packet_loss_iperf_core_1000.csv](https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/blob/main/cloudlab-outputs/packet_loss_iperf_core_1000.csv)
  2. 'output_mathis_C_iperf.csv' has the total bandwidth, total number of retransmits, total congestion window halving events, 'C' value using packet loss rate, 'C' value using congestion window halving rate, ratio of packets dropped at the router to congestion window halving event.

     Example output from running the command is [output_mathis_C_iperf.csv](https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/blob/main/cloudlab-outputs/output_mathis_C_iperf.csv)
     `time_interval,time_duration,ports,sum(y_values),total_cwnd_half,total_retransmission,total_retransmission/total_cwnd_half,np.nanmean(list_ratio),reg_simple1.intercept_,reg_simple1.coef_[0],reg_simple2.intercept_,reg_simple2.coef_[0],router_dropped,router_sent,router_dropped/total_cwnd_half
0.01,1800,1000,10045527000,328005,150056,0.457480831084892,0.4592942121018375,0.0,2.6682251202316913,0.0,3.985303969272882,98829,1686597751,0.30130333379064345`
  3. 'linear_reg_plot.pdf' contains two plots showing
     
     a. x=mss/rtt\*sqrt(packet loss rate) vs actual bandwidth per flow; regression line and x=mss/rtt\*sqrt(packet loss rate) vs predicted bandwidth per flow.
     
     b. x=mss/rtt\*sqrt(cwnd halving rate) vs actual bandwidth per flow; linear regression line and x=mss/rtt\*sqrt(cwnd halving rate) vs predicted bandwidth per flow.
     
      Example output from running the command is [linear_reg_plot_core_1000.pdf](https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/blob/main/cloudlab-outputs/linear_reg_plot_core_1000.pdf) 

* On the router: run `bash /local/repository/cloudlab-scripts/setup-edge.sh` and confirm that you see about **100 Mbps** sum throughput for multiple flows (on average 10 Mbps for each of the 10 flows), 100 Mbps throughput for single flow, and 0-2 ms RTT.
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 1 1800 reno 1 0.01` to to generate 10 flows with 20ms delay. To change the number of flows to 30 and 50, change the 7th parameter from 1 to 3 and 5 respectively. Three files are generated-
  1. 'packet_loss_iperf.csv' which has the mean rtt, bandwidth, number of retransmits, number of congestion window halving events, packet loss rate and congestion window halving rate for each flow.

     Example output file from running the command is [packet_loss_iperf_edge_10.csv](https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/blob/main/cloudlab-outputs/packet_loss_iperf_edge_10.csv)
  2. 'output_mathis_C_iperf.csv' has the total bandwidth, total number of retransmits, total congestion window halving events, 'C' value using packet loss rate, 'C' value using congestion window halving rate, ratio of packets dropped at the router to congestion window halving event.
     `time_interval,time_duration,ports,sum(y_values),total_cwnd_half,total_retransmission,total_retransmission/total_cwnd_half,np.nanmean(list_ratio),reg_simple1.intercept_,reg_simple1.coef_[0],reg_simple2.intercept_,reg_simple2.coef_[0],router_dropped,router_sent,router_dropped/total_cwnd_half
0.01,1800,10,95791000,3588,2064,0.5752508361204013,0.5827833785106743,0.0,2.473642492258249,0.0,3.2641250718214074,1223,15413505,0.34085841694537344`

     Example output from running the command is [output_mathis_C_iperf.csv](https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/blob/main/cloudlab-outputs/output_mathis_C_iperf.csv)
     
  3. 'linear_reg_plot.pdf' contains two plots showing
     
     a. x=mss/rtt\*sqrt(packet loss rate) vs actual bandwidth per flow; regression line and x=mss/rtt\*sqrt(packet loss rate) vs predicted bandwidth per flow.
  
     b. x=mss/rtt\*sqrt(cwnd halving rate) vs actual bandwidth per flow; linear regression line and x=mss/rtt\*sqrt(cwnd halving rate) vs predicted bandwidth per flow.

      Example output from running the command is [linear_reg_plot_edge_10.pdf](https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/blob/main/cloudlab-outputs/linear_reg_plot_edge_10.pdf)

To validate this finding on FABRIC:

* In the Jupyter environment, select File > New > Terminal and in this terminal, run `https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP`
* Open fabric-notebook subdirectory inside IMC directory.
* Run the notebook `00-reserve.ipynb` to reserve the resources. This will reserve 10 sender-reciver pair and a router. All the required dependencies or modules will be installed. [Example notebook](https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/blob/main/fabric-outputs/00-reserve.ipynb)
* Run the notebook `01-validate.ipynb' and confirm that you see about 24-28 Gbps sum throughput for multiple flows (on average 2.5 Gbps for each of the 10 flows), 8-17 Gbps throughput for single flow, and 0-1 ms RTT.
[Example notebook](https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/blob/main/fabric-outputs/01-validate.ipynb)
* Run the notebook `02-setup-core.ipynb` and confirm that you see about **10 Gbps** sum throughput for multiple flows (on average 1 Gbps for each of the 10 flows), 8-10 Gbps throughput for single flow, and 0-2 ms RTT. 
[Example notebook](https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/blob/main/fabric-outputs/02-setup-core.ipynb)

* Run the notebook `get_mathis_constant.ipynb`. Set the parameters as mentioned in the notebook to run experiments with reno at 20ms delay  
[Example notebook](https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/blob/main/fabric-outputs/get_mathis_constant.ipynb)

* Run the notebook `04-setup-edge.ipynb` and confirm that you see about **100 Mbps** sum throughput for multiple flows (on average 10 Mbps for each of the 10 flows), 100 Mbps throughput for single flow, and 0-2 ms RTT. 
[Example notebook](https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/blob/main/fabric-outputs/04-setup-edge.ipynb)
* Run the notebook `get_mathis_constant.ipynb`. Vary the parameters as mentioned in the notebook to run experiments with reno at 20ms delay.

Discussion:

The finding from the original paper is shown below which states "Deriving the Mathis constant 𝐶 using the packet loss rate results in different flow count-dependent constants in CoreScale vs EdgeScale, while using the CWND halving rate results in consistent values across settings and flow counts"

<img width="453" alt="image" src="https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/assets/91571551/c4009c9e-2215-4e38-ac46-ce8102a445ee">

Following is the result of the experiment: We found that the Mathis constant C using packet loss rate results in flow count-independent constant in CoreScale and EdgeScale, while using CWND halving rate results in flow count-dependent constant in CoreScale and EdgeScale. 

<img width="453" alt="image" src="https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/assets/91571551/3d402c02-d7ae-489f-a8ce-1d1a8c2415d0">

As per the original paper, the variation in Mathis Constant C is due to the ratio of packet loss to CWND halving rate not being constant at the CoreScale. In EdgeScale, the ratio of packet losses to CWND halvings is approximately 1.7 regardless of the number of concurrent flows. But in CoreScale the ratio varies between 6 and 9 and depends on the flow count.   

<img width="453" alt="image" src="https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/assets/91571551/b5eea1db-cc99-4b02-935f-afa1e6268971">

Experiment results from CloudLab:
Our experiment shows that the ratio between packet loss to CWND halving rate is a constant at both EdgeScale and CoreScale.

<img width="441" alt="image" src="https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/assets/91571551/9dc525fd-c8a8-42e4-b2f8-704f7fba0c39">

<img width="479" alt="image" src="https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/assets/91571551/3a00a5c2-32a3-4205-9b55-86b83f908be4">

Data source of above graphs is at [Mathis_Constant_CloudLab.csv](https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/blob/main/cloudlab-outputs/Mathis_Constant.csv).

Experiment results from FABRIC:

[Mathis_Constant.csv](https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/blob/main/fabric-outputs/Mathis_C_FABRIC.csv)



## Finding 2

> NewReno and Cubic show high intra-CCA fairness in CoreScale, in line with past research. BBR shows poor intra-CCA fairness in CoreScale, contradicting previous research in the edge setting.

To validate this finding on CloudLab:

* Open the [CloudLab profile](https://www.cloudlab.us/p/nyunetworks/imc-revisiting). Leave parameters at their default settings, and reserve resources at CloudLab Utah. Wait for resources to come up and for startup scripts to be complete. Open an SSH terminal at the router.
* On the router: run `bash /local/repository/cloudlab-scripts/validate.sh` and confirm that you see about 24-25 Gbps sum throughput for multiple flows (on average 2.5 Gbps for each of the 10 flows), 8-10 Gbps throughput for single flow, and 0-1 ms RTT.
* On the router: run `bash /local/repository/cloudlab-scripts/setup-core.sh` and confirm that you see about **10 Gbps** sum throughput for multiple flows (on average 1 Gbps for each of the 10 flows), 7-10 Gbps throughput for single flow, and 0-2 ms RTT.
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 10 1800 reno 10 1`.
  'jfi.csv' file is created (if there is none otherwise append the current result in new line). It has cca, duration of expt(sec), base RTT(ms)', total bandwidth(Kbps), sum of square of bandwidth, flow count and JFI.

  Example output from running the command is 
  `CCA,Duration of Expt(sec),Base RTT(ms),Total Bandwidth(Kbps),Sum of sq of BW,Flow Count,JFI
  reno,1800,20,10045527,102111493807,1000,0.9882590974377773`
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 10 1800 cubic 10 1`.
  
  Example output from running the command is
  `CCA,Duration of Expt(sec),Base RTT(ms),Total Bandwidth(Kbps),Sum of sq of BW,Flow Count,JFI
  cubic,1800,20,10204264,105839294552,1000,0.9838217858730839`
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 10 1800 bbr 10 1`.
  
  Example output from running the command is
  CCA,Duration of Expt(sec),Base RTT(ms),Total Bandwidth(Kbps),Sum of sq of BW,Flow Count,JFI
  bbr,1800,20,9903756,101231459864,1000,0.9689120658667576`
  
* On the router: run `bash /local/repository/cloudlab-scripts/setup-edge.sh` and confirm that you see about **100 Mbps** sum throughput for multiple flows (on average 10 Mbps for each of the 10 flows), 100 Mbps throughput for single flow, and 0-2 ms RTT.
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 1 1800 reno 1 1`.

  Example output from running the command is
  `CCA,Duration of Expt(sec),Base RTT(ms),Total Bandwidth(Kbps),Sum of sq of BW,Flow Count,JFI
  reno,1800,20,95791,922660429,10,0.9945062552368332`
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 1 1800 cubic 1 1`.
  
  Example output from running the command is
  `CCA,Duration of Expt(sec),Base RTT(ms),Total Bandwidth(Kbps),Sum of sq of BW,Flow Count,JFI
  cubic,1800,20,95879,935617695,10,0.9825362100489132`  
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 1 1800 bbr 1 1`.

  Example output from running the command is
  `CCA,Duration of Expt(sec),Base RTT(ms),Total Bandwidth(Kbps),Sum of sq of BW,Flow Count,JFI
  bbr,1800,20,94261,889051487,10,0.9993950014055822`

  Combined output of all the above experiment can be found at [JFI.csv](https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/blob/main/cloudlab-outputs/jfi.csv)

To validate this finding on FABRIC:

* In the Jupyter environment, select File > New > Terminal and in this terminal, run `https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP`
* Open fabric-notebook subdirectory inside IMC directory.
* Run the notebook `00-reserve.ipynb` to reserve the resources. This will reserve 10 sender-reciver pair and a router. All the required dependencies or modules will be installed.
[Example notebook](https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/blob/main/fabric-outputs/00-reserve.ipynb)
* Run the notebook `01-validate.ipynb' and confirm that you see about 24-28 Gbps sum throughput for multiple flows (on average 2.5 Gbps for each of the 10 flows), 8-17 Gbps throughput for single flow, and 0-1 ms RTT.
[Example notebook](https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/blob/main/fabric-outputs/01-validate.ipynb)
* Run the notebook `02-setup-core.ipynb` and confirm that you see about **10 Gbps** sum throughput for multiple flows (on average 1 Gbps for each of the 10 flows), 7-10 Gbps throughput for single flow, and 0-2 ms RTT. 
[Example notebook](https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/blob/main/fabric-outputs/02-setup-core.ipynb)
* Run the notebook `intra-cca-fairness.ipynb`. Vary the parameters as mentioned in the notebook to run experiments with reno, bbr and cubic.
[Example notebook](https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/blob/main/fabric-outputs/intra-cca-fairness.ipynb)
* Run the notebook `04-setup-edge.ipynb` and confirm that you see about **100 Mbps** sum throughput for multiple flows (on average 10 Mbps for each of the 10 flows), 100 Mbps throughput for single flow, and 0-2 ms RTT. 
[Example notebook](https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/blob/main/fabric-outputs/04-setup-edge.ipynb)
* Run the notebook `intra-cca-fairness.ipynb`. Vary the parameters as mentioned in the notebook to run experiments with reno, bbr and cubic.

  
Discussion: 
As per original paper:
1. NewReno & Cubic continue to show high intra-CCA fairness in CoreScale with a JFI > 0.99, as expected from past research.
2. BBR surprisingly shows intra-CCA unfairness in CoreScale, with JFIs as low as 0.4, which is not expected from past research. Milder unfairness also occurs when more than 10 flows compete in EdgeScale, with JFI’s as low as 0.7.
   <img width="441" alt="image" src="https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/assets/91571551/38fb619e-5abf-42a7-abe6-c35e918497e9">

As per experiment on CloudLab:
1. NewReno and Cubic show high intra-CCA fairness in CoreScale and EdgeScale with a JFI > 0.95
2. BBR shows intra-CCA fairness in both EdgeScale and CoreScale with JFI > 0.95
Reno:
<img width="678" alt="image" src="https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/assets/91571551/d1bf1bbd-62f3-48ac-956c-4c3748df1822">

Cubic:
<img width="678" alt="image" src="https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/assets/91571551/9a6d45ac-0e35-4753-bc05-bd1047f3048e">

BBR:
<img width="678" alt="image" src="https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/assets/91571551/e400cc0d-833e-4733-8545-4690c0ee64d7">

Data source of all above plots is [JFI_cloudlab.csv](https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/blob/main/cloudlab-outputs/JFI_cloudlab.csv)


As per experiment on FABRIC:
1. NewReno and Cubic show high intra-CCA fairness in CoreScale and EdgeScale with a JFI > 0.91
2. BBR shows intra-CCA fairness in both EdgeScale and CoreScale with JFI > 0.92
Reno:
<img width="678" alt="image" src="https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/assets/91571551/ed3c9e9b-c487-4b6b-83bb-e2778ba21442">

Cubic:
<img width="678" alt="image" src="https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/assets/91571551/71e90e81-afd6-4a7d-92a7-eb3c2e89340a">


BBR:
<img width="678" alt="image" src="https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/assets/91571551/7e74faca-e6b3-4704-a7a4-01e77cfb43d8">

Data source of all above plots is [JFI_FABRIC.csv](https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/blob/main/fabric-outputs/JFI_FABRIC.csv)


## Finding 3

> Cubic achieves 70 to 80% of total throughput when competing with an equal number of NewReno flows at CoreScale, while BBR is highly unfair to loss-based CCA, i.e., NewReno and Cubic. These results are in line with past research in the edge setting.

To validate this finding on CloudLab:

TBD

To validate this finding on FABRIC:

TBD

Discussion: 

TBD

## Extension to intermediate settings

### Finding 1
> The Mathis model for TCP NewReno throughput is valid at CoreScale only if the congestion event rate (p) and model parameter C are calculated using the CWND-halving rate, rather than the conventional packet loss rate that is typically used for EdgeScale.

To validate this finding on CloudLab:

* Open the [CloudLab profile](https://www.cloudlab.us/p/nyunetworks/imc-revisiting). Leave parameters at their default settings, and reserve resources at CloudLab Utah. Wait for resources to come up and for startup scripts to be complete. Open an SSH terminal at the router.
* On the router: run `bash /local/repository/cloudlab-scripts/validate.sh` and confirm that you see about 24-25 Gbps sum throughput for multiple flows (on average 2.5 Gbps for each of the 10 flows), 8-10 Gbps throughput for single flow, and 0-1 ms RTT.
* Run the notebook `03-setup-intermediate.ipynb` and confirm that you see about **1 Gbps** sum throughput for multiple flows (on average 100 Mbps for each of the 10 flows), 1 Gbps throughput for single flow, and 0-2 ms RTT.
* * On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 10 1800 reno 1 0.01` to generate 100 flows with 20ms delay. To change the number of flows to 300 and 500, change the 7th parameter from 1 to 3 and 5 respectively. Three files are generated-
  1. 'packet_loss_iperf.csv' which has the mean rtt, bandwidth, number of retransmits, number of congestion window halving events, packet loss rate and congestion window halving rate for each flow.

     Example output file from running the command is [packet_loss_iperf_core_1000.csv](https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/blob/main/cloudlab-outputs/packet_loss_iperf_core_1000.csv)
  2. 'output_mathis_C_iperf.csv' has the total bandwidth, total number of retransmits, total congestion window halving events, 'C' value using packet loss rate, 'C' value using congestion window halving rate, ratio of packets dropped at the router to congestion window halving event.

     Example output from running the command is [output_mathis_C_iperf.csv](https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/blob/main/cloudlab-outputs/output_mathis_C_iperf.csv)
     `time_interval,time_duration,ports,sum(y_values),total_cwnd_half,total_retransmission,total_retransmission/total_cwnd_half,np.nanmean(list_ratio),reg_simple1.intercept_,reg_simple1.coef_[0],reg_simple2.intercept_,reg_simple2.coef_[0],router_dropped,router_sent,router_dropped/total_cwnd_half
0.01,1800,1000,10045527000,328005,150056,0.457480831084892,0.4592942121018375,0.0,2.6682251202316913,0.0,3.985303969272882,98829,1686597751,0.30130333379064345`
  3. 'linear_reg_plot.pdf' contains two plots showing
     
     a. x=mss/rtt\*sqrt(packet loss rate) vs actual bandwidth per flow; regression line and x=mss/rtt\*sqrt(packet loss rate) vs predicted bandwidth per flow.
     
     b. x=mss/rtt\*sqrt(cwnd halving rate) vs actual bandwidth per flow; linear regression line and x=mss/rtt\*sqrt(cwnd halving rate) vs predicted bandwidth per flow.
     
      Example output from running the command is [linear_reg_plot_core_1000.pdf](https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/blob/main/cloudlab-outputs/linear_reg_plot_core_1000.pdf)




     
[Example notebook](https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/blob/main/fabric-outputs/04-setup-edge.ipynb)
* Run the notebook `intra-cca-fairness.ipynb`. Vary the parameters as mentioned in the notebook to run experiments with reno, bbr and cubic.
