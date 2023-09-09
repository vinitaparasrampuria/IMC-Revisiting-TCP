# Revisiting TCP CCA
Study of Fairness and throughput for TCP Reno, CUBIC and BBR in high scale network.

---

## Finding 1

> The Mathis model for TCP NewReno throughput is valid at CoreScale only if the congestion event rate (p) and model parameter C are calculated using the CWND-halving rate, rather than the conventional packet loss rate that is typically used for EdgeScale.

To validate this finding on CloudLab:

* Open the [CloudLab profile](https://www.cloudlab.us/p/nyunetworks/imc-revisiting). Leave parameters at their default settings, and reserve resources at CloudLab Utah. Wait for resources to come up and for startup scripts to be complete. Open an SSH terminal at the router.
* On the router: run `bash /local/repository/cloudlab-scripts/validate.sh` and confirm that you see about 24-25 Gbps sum throughput for multiple flows (on average 2.5 Gbps for each of the 10 flows), 5-8 Gbps throughput for single flow, and 0-1 ms RTT. [Sample output](https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/blob/main/cloudlab-outputs/validate_output.txt)
* On the router: run `bash /local/repository/cloudlab-scripts/setup-core.sh` and confirm that you see about **10 Gbps** sum throughput for multiple flows (on average 1 Gbps for each of the 10 flows), 5-8 Gbps throughput for single flow, and 0-2 ms RTT.[Sample output](https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/blob/main/cloudlab-outputs/setup_core_output.txt)
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 100 3600 reno 1 0.01 0` to generate 1000 flows. Two files are generated-

  1. 'output_mathis_C.csv' has the total bandwidth, total number of retransmits, total congestion window halving events, 'C' value using packet loss rate, 'C' value using congestion window halving rate, ratio of packets dropped at the router to congestion window halving event.
     Example output from running the command is:
`time_duration,ports,Base_RTT(ms),BW,total_data_seg_out,total_cwnd_half,total_retransmission_ss,total_retransmission_iperf,total_retransmission_ss/total_cwnd_half,total_retransmission_iperf/total_cwnd_half,C_ss,C_iperf,C_cwnd,C_router,router_dropped,router_sent,router_dropped/total_cwnd_half,mdape_ss,mdape_iperf,mdape_cwnd,mdape_router`
3600,1000,20,8780200,2727843242,75864,359609,359609,4.740179795423389,4.740179795423389,2.745428755706345,2.745428755706345,1.3284517297454073,2.7397654145890655,321576,2728417668,4.238848465675419,11.588264929085723,11.588264929085723,1.331712875334782,6.0975053627026


  2. 'linear_reg_plot.pdf' contains four plots showing:
     a. x=mss/rtt\*sqrt(packet loss rate from ss data) vs actual bandwidth per flow; regression line and x=mss/rtt\*sqrt(packet loss rate from ss data) vs predicted bandwidth per flow.
     b. x=mss/rtt\*sqrt(packet loss rate from iperf3 data) vs actual bandwidth per flow; regression line and x=mss/rtt\*sqrt(packet loss rate from iperf3 data) vs predicted bandwidth per flow.
     c. x=mss/rtt\*sqrt(cwnd halving rate) vs actual bandwidth per flow; linear regression line and x=mss/rtt\*sqrt(cwnd halving rate) vs predicted bandwidth per flow.
     d. x=mss/rtt\*sqrt(packet loss rate at router) vs actual bandwidth per flow; regression line and x=mss/rtt\*sqrt(packet loss rate at router) vs predicted bandwidth per flow.
      Example output from running the command is [linear_reg_plot_1000.pdf](https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/blob/main/cloudlab-outputs/Plots/Linear-Regression-plots/linear_reg_plot_1000.pdf).
      
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 300 3600 reno 1 0.01 0` to generate 3000 flows. Two files are updated/generated-
  1. A new line is added at the last to existing 'output_mathis_C.csv' with the current results
     Example output from running the command is:
`3600,3000,20,8616034,2675407004,622473,1949503,1949474,3.1318675669466787,3.1318209785805973,2.239721731399115,2.239712118320674,1.2866032896686965,2.2651717616729408,1928296,2676745022,3.0977986193778686,5.681361524395942,5.680907930896435,0.9533862885352663,3.430406097825095`


  2. 'linear_reg_plot.pdf' contains four plots showing:
     a. x=mss/rtt\*sqrt(packet loss rate from ss data) vs actual bandwidth per flow; regression line and x=mss/rtt\*sqrt(packet loss rate from ss data) vs predicted bandwidth per flow.
     b. x=mss/rtt\*sqrt(packet loss rate from iperf3 data) vs actual bandwidth per flow; regression line and x=mss/rtt\*sqrt(packet loss rate from iperf3 data) vs predicted bandwidth per flow.
     c. x=mss/rtt\*sqrt(cwnd halving rate) vs actual bandwidth per flow; linear regression line and x=mss/rtt\*sqrt(cwnd halving rate) vs predicted bandwidth per flow.
     d. x=mss/rtt\*sqrt(packet loss rate at router) vs actual bandwidth per flow; regression line and x=mss/rtt\*sqrt(packet loss rate at router) vs predicted bandwidth per flow.
      Example output from running the command is [linear_reg_plot_3000.pdf](https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/blob/main/cloudlab-outputs/Plots/Linear-Regression-plots/linear_reg_plot_3000.pdf).

* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 500 3600 reno 1 0.01 0` to generate 5000 flows. Two files are updated/generated-

  1. A new line is added at the last to existing 'output_mathis_C.csv' with the current results
     Example output from running the command is 
    `3600,5000,20,8665154,2682578560,1636004,4209106,4212199,2.5727968880271685,2.5746874702017846,2.021965112407632,2.022710516447602,1.2685571957267616,2.0254296430186725,4183131,2691737751,2.5569197874821823,3.7512171301968813,3.786478793533293,1.2271553551082046,2.651727726488693`

  2. 'linear_reg_plot.pdf' contains four plots showing:
     a. x=mss/rtt\*sqrt(packet loss rate from ss data) vs actual bandwidth per flow; regression line and x=mss/rtt\*sqrt(packet loss rate from ss data) vs predicted bandwidth per flow.
     b. x=mss/rtt\*sqrt(packet loss rate from iperf3 data) vs actual bandwidth per flow; regression line and x=mss/rtt\*sqrt(packet loss rate from iperf3 data) vs predicted bandwidth per flow.
     c. x=mss/rtt\*sqrt(cwnd halving rate) vs actual bandwidth per flow; linear regression line and x=mss/rtt\*sqrt(cwnd halving rate) vs predicted bandwidth per flow.
     d. x=mss/rtt\*sqrt(packet loss rate at router) vs actual bandwidth per flow; regression line and x=mss/rtt\*sqrt(packet loss rate at router) vs predicted bandwidth per flow.
      Example output from running the command is [linear_reg_plot_5000.pdf](https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/blob/main/cloudlab-outputs/Plots/Linear-Regression-plots/linear_reg_plot_5000.pdf)

* On the router: run `bash /local/repository/cloudlab-scripts/setup-edge.sh` and confirm that you see about **100 Mbps** sum throughput for multiple flows (on average 10 Mbps for each of the 10 flows), 100 Mbps throughput for single flow, and 0-2 ms RTT.
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 1 10800 reno 1 0.01 0` to to generate 10 flows. Two files are updated/generated-
  1. A new line is added at the last to existing 'output_mathis_C.csv' with the current results
     Example output from running the command is
    10800,10,20,95732,89259100,4009,9179,9179,2.2895984035919184,2.2895984035919184,1.9007098126863524,1.9007098126863524,1.2875252082863067,1.9516285900399155,9179,89257163,2.2895984035919184,10.294811974731441,10.294811974731441,0.2559681693187176,5.276366012422708

  2. 'linear_reg_plot.pdf' contains four plots showing:
     a. x=mss/rtt\*sqrt(packet loss rate from ss data) vs actual bandwidth per flow; regression line and x=mss/rtt\*sqrt(packet loss rate from ss data) vs predicted bandwidth per flow.
     b. x=mss/rtt\*sqrt(packet loss rate from iperf3 data) vs actual bandwidth per flow; regression line and x=mss/rtt\*sqrt(packet loss rate from iperf3 data) vs predicted bandwidth per flow.
     c. x=mss/rtt\*sqrt(cwnd halving rate) vs actual bandwidth per flow; linear regression line and x=mss/rtt\*sqrt(cwnd halving rate) vs predicted bandwidth per flow.
     d. x=mss/rtt\*sqrt(packet loss rate at router) vs actual bandwidth per flow; regression line and x=mss/rtt\*sqrt(packet loss rate at router) vs predicted bandwidth per flow.
      Example output from running the command is [linear_reg_plot_10.pdf](https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/blob/main/cloudlab-outputs/Plots/Linear-Regression-plots/linear_reg_plot_10.pdf)

  * On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 3 10800 reno 1 0.01 0` to to generate 30 flows. Two files are updated/generated-
  1. A new line is added at the last to existing 'output_mathis_C.csv' with the current results
     Example output from running the command is 
  `10800,30,20,95763,89333740,32736,64839,64839,1.9806634897360704,1.9806634897360704,1.7580713003941804,1.7580713003941804,1.2591796470166545,1.7761195222068231,64839,89276541,1.9806634897360704,2.816221353874746,2.816221353874746,0.21917187404515756,3.8241736234131642`

  2. 'linear_reg_plot.pdf' contains four plots showing:
     a. x=mss/rtt\*sqrt(packet loss rate from ss data) vs actual bandwidth per flow; regression line and x=mss/rtt\*sqrt(packet loss rate from ss data) vs predicted bandwidth per flow.
     b. x=mss/rtt\*sqrt(packet loss rate from iperf3 data) vs actual bandwidth per flow; regression line and x=mss/rtt\*sqrt(packet loss rate from iperf3 data) vs predicted bandwidth per flow.
     c. x=mss/rtt\*sqrt(cwnd halving rate) vs actual bandwidth per flow; linear regression line and x=mss/rtt\*sqrt(cwnd halving rate) vs predicted bandwidth per flow.
     d. x=mss/rtt\*sqrt(packet loss rate at router) vs actual bandwidth per flow; regression line and x=mss/rtt\*sqrt(packet loss rate at router) vs predicted bandwidth per flow.
      Example output from running the command is [linear_reg_plot_30.pdf](https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/blob/main/cloudlab-outputs/Plots/Linear-Regression-plots/linear_reg_plot_30.pdf).

* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 5 10800 reno 1 0.01 0` to to generate 50 flows. Two files are updated/generated-
  1. A new line is added at the last to existing 'output_mathis_C.csv' with the current results
     Example output from running the command is
`10800,50,20,95709,89381941,85694,161653,161653,1.8863981142203654,1.8863981142203654,1.6881173177937583,1.6881173177937583,1.2371940831402188,1.7023918930828428,161653,89228732,1.8863981142203654,1.4047534030313038,1.4047534030313038,0.24674646924651156,3.9534236802158356`

  2. 'linear_reg_plot.pdf' contains four plots showing:
     a. x=mss/rtt\*sqrt(packet loss rate from ss data) vs actual bandwidth per flow; regression line and x=mss/rtt\*sqrt(packet loss rate from ss data) vs predicted bandwidth per flow.
     b. x=mss/rtt\*sqrt(packet loss rate from iperf3 data) vs actual bandwidth per flow; regression line and x=mss/rtt\*sqrt(packet loss rate from iperf3 data) vs predicted bandwidth per flow.
     c. x=mss/rtt\*sqrt(cwnd halving rate) vs actual bandwidth per flow; linear regression line and x=mss/rtt\*sqrt(cwnd halving rate) vs predicted bandwidth per flow.
     d. x=mss/rtt\*sqrt(packet loss rate at router) vs actual bandwidth per flow; regression line and x=mss/rtt\*sqrt(packet loss rate at router) vs predicted bandwidth per flow.

     The combined output of all the experiments can be found at [C_CloudLab.csv](https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/blob/main/cloudlab-outputs/C_CloudLab.csv)
     Linear regression plots are available at [Linear_Regression_Plots](https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/tree/main/cloudlab-outputs/Plots/Linear-Regression-plots)

To validate this finding on FABRIC:

* In the Jupyter environment, select File > New > Terminal and in this terminal, run `git clone https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP`
* Open fabric-notebook subdirectory inside IMC directory.
* Run the notebook `00-reserve.ipynb` to reserve the resources. This will reserve 10 sender-reciver pair and a router. All the required dependencies or modules will be installed.
* Run the notebook `01-validate.ipynb' and confirm that you see about 24-28 Gbps sum throughput for multiple flows (on average 2.5 Gbps for each of the 10 flows), 8-17 Gbps throughput for single flow, and 0-1 ms RTT.
* Run the notebook `02-setup-core.ipynb` and confirm that you see about **10 Gbps** sum throughput for multiple flows (on average 1 Gbps for each of the 10 flows), 8-10 Gbps throughput for single flow, and 0-2 ms RTT. 
* Run the notebook `05-get-mathis-constant.ipynb`. Set the parameters in the notebook under 'Set experiment parameters' as mentioned below to run experiments with 1000 reno flows.
cca="reno"; delay=20; test_duration=3600; num_servers=100; flows=1; interval=0.01; omit=0
* Run the notebook `05-get-mathis-constant.ipynb`. Set the parameters in the notebook under 'Set experiment parameters' as mentioned below to run experiments with 3000 reno flows.
cca="reno"; delay=20; test_duration=3000; num_servers=300; flows=1; interval=0.01; omit=0
* Run the notebook `05-get-mathis-constant.ipynb`. Set the parameters in the notebook under 'Set experiment parameters' as mentioned below to run experiments with 5000 reno flows.
cca="reno"; delay=20; test_duration=1800; num_servers=500; flows=1; interval=0.01; omit=0
* Run the notebook `04-setup-edge.ipynb` and confirm that you see about **100 Mbps** sum throughput for multiple flows (on average 10 Mbps for each of the 10 flows), 100 Mbps throughput for single flow, and 0-2 ms RTT. 
* Run the notebook `05-get-mathis-constant.ipynb`. Set the parameters in the notebook under 'Set experiment parameters' as mentioned below to run experiments with 10 reno flows.
cca="reno"; delay=20; test_duration=10800; num_servers=1; flows=1; interval=0.01; omit=0
* Run the notebook `05-get-mathis-constant.ipynb`. Set the parameters in the notebook under 'Set experiment parameters' as mentioned below to run experiments with 30 reno flows.
cca="reno"; delay=20; test_duration=10800; num_servers=3; flows=1; interval=0.01; omit=0
* Run the notebook `05-get-mathis-constant.ipynb`. Set the parameters in the notebook under 'Set experiment parameters' as mentioned below to run experiments with 50 reno flows.
cca="reno"; delay=20; test_duration=10800; num_servers=5; flows=1; interval=0.01; omit=0

The output of all the above experiments can be found at [C_FABRIC.csv](https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/blob/main/fabric-outputs/C_FABRIC.csv)
All the regression plots are available at [Linear-regression-plots](https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/tree/main/fabric-outputs/Plots/Linear-Regression-Plots)


Discussion:

The finding from the original paper is shown below which states "Deriving the Mathis constant 𝐶 using the packet loss rate results in different flow count-dependent constants in CoreScale vs EdgeScale, while using the CWND halving rate results in consistent values across settings and flow counts"

<img width="453" alt="image" src="https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/assets/91571551/c4009c9e-2215-4e38-ac46-ce8102a445ee">

Following is the result of the experiment: 
CloudLab:
Our experiment validates the original findings and CWND halving rate results in flow count-independent constant in CoreScale and EdgeScale. 

<img width="486" alt="image" src="https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/assets/91571551/c924f980-7ab8-4ad1-8c1a-7bcdbb085c16">

FABRIC:
Our experiment validates the original findings and CWND halving rate results in flow count-independent constant in CoreScale and EdgeScale. 

<img width="528" alt="image" src="https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/assets/91571551/29adf722-36f3-4834-97b1-bee7a35a0346">


As per the original paper, the variation in Mathis Constant C is due to the ratio of packet loss to CWND halving rate not being constant at the CoreScale. In EdgeScale, the ratio of packet losses to CWND halvings is approximately 1.7 regardless of the number of concurrent flows. But in CoreScale the ratio varies between 6 and 9 and depends on the flow count.   

<img width="453" alt="image" src="https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/assets/91571551/b5eea1db-cc99-4b02-935f-afa1e6268971">

CloudLab:
Our experiment shows that the ratio between packet loss to CWND halving rate is almost constant at EdgeScale but varies in CoreScale.

<img width="595" alt="image" src="https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/assets/91571551/1320a24d-4320-4e08-aa90-492e9f152db5">

<img width="595" alt="image" src="https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/assets/91571551/3ccea454-00fe-4b3f-963d-3ea90fb4e786">


Data source of above graphs is at [C_CloudLab.csv](https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/blob/main/cloudlab-outputs/C_CloudLab.csv)

FABRIC:

Our experiment shows that the ratio between packet loss to CWND halving rate is almost constant at CoreScale but varies in EdgeScale.

<img width="587" alt="image" src="https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/assets/91571551/d3cbd3f2-752b-44a4-9b17-5c94b8e7171e">

<img width="587" alt="image" src="https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/assets/91571551/d3add098-2a5c-4893-99e5-8bd5fb137415">



Data source of above graphs is at [C_CloudLab.csv](https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/blob/main/cloudlab-outputs/C_CloudLab.csv)
Data source of above graphs is at [C_FABRIC.csv](https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/blob/main/fabric-outputs/C_FABRIC.csv)



## Finding 2

> NewReno and Cubic show high intra-CCA fairness in CoreScale, in line with past research. BBR shows poor intra-CCA fairness in CoreScale, contradicting previous research in the edge setting.

To validate this finding on CloudLab:

* Open the [CloudLab profile](https://www.cloudlab.us/p/nyunetworks/imc-revisiting). Leave parameters at their default settings, and reserve resources at CloudLab Utah. Wait for resources to come up and for startup scripts to be complete. Open an SSH terminal at the router.
* On the router: run `bash /local/repository/cloudlab-scripts/validate.sh` and confirm that you see about 24-25 Gbps sum throughput for multiple flows (on average 2.5 Gbps for each of the 10 flows), 5-8 Gbps throughput for single flow, and 0-1 ms RTT. [Sample output](https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/blob/main/cloudlab-outputs/validate_output.txt)
* On the router: run `bash /local/repository/cloudlab-scripts/setup-core.sh` and confirm that you see about **10 Gbps** sum throughput for multiple flows (on average 1 Gbps for each of the 10 flows), 5-8 Gbps throughput for single flow, and 0-2 ms RTT.[Sample output](https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/blob/main/cloudlab-outputs/setup_core_output.txt)
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 100 10800 bbr 1 1 0` to generate 1000 bbr flows at 20ms delay.
  'jfi.csv' file is created (if there is none otherwise append the current result in new line). It has cca, duration of expt(sec), base RTT(ms)', total bandwidth(Kbps), sum of square of bandwidth, flow count and JFI.
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 300 10800 bbr 1 1 0` to generate 3000 bbr flows at 20ms delay.
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 500 10800 bbr 1 1 0` to generate 5000 bbr flows at 20ms delay.
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 100 10800 bbr 1 1 0` to generate 1000 bbr flows at 100ms delay.
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 300 10800 bbr 1 1 0` to generate 3000 bbr flows at 100ms delay.
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 500 10800 bbr 1 1 0` to generate 5000 bbr flows at 100ms delay.
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 100 10800 bbr 1 1 0` to generate 1000 bbr flows at 200ms delay.
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 300 10800 bbr 1 1 0` to generate 3000 bbr flows at 200ms delay.
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 500 10800 bbr 1 1 0` to generate 5000 bbr flows at 200ms delay.
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 100 10800 cubic 1 1 0` to generate 1000 cubic flows at 20ms delay.
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 300 10800 cubic 1 1 0` to generate 3000 cubic flows at 20ms delay.
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 500 10800 cubic 1 1 0` to generate 5000 cubic flows at 20ms delay.
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 100 10800 cubic 1 1 0` to generate 1000 cubic flows at 100ms delay.
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 300 10800 cubic 1 1 0` to generate 3000 cubic flows at 100ms delay.
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 500 10800 cubic 1 1 0` to generate 5000 cubic flows at 100ms delay.
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 100 10800 cubic 1 1 0` to generate 1000 cubic flows at 200ms delay.
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 300 10800 cubic 1 1 0` to generate 3000 cubic flows at 200ms delay.
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 500 10800 cubic 1 1 0` to generate 5000 cubic flows at 200ms delay.
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 100 10800 reno 1 1 0` to generate 1000 reno flows at 20ms delay.
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 300 10800 reno 1 1 0` to generate 3000 reno flows at 20ms delay.
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 500 10800 reno 1 1 0` to generate 5000 reno flows at 20ms delay.
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 100 10800 reno 1 1 0` to generate 1000 reno flows at 100ms delay.
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 300 10800 reno 1 1 0` to generate 3000 reno flows at 100ms delay.
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 500 10800 reno 1 1 0` to generate 5000 reno flows at 100ms delay.
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 100 10800 reno 1 1 0` to generate 1000 reno flows at 200ms delay.
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 300 10800 reno 1 1 0` to generate 3000 reno flows at 200ms delay.
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 500 10800 reno 1 1 0` to generate 5000 reno flows at 200ms delay.
  
  
* On the router: run `bash /local/repository/cloudlab-scripts/setup-edge.sh` and confirm that you see about **100 Mbps** sum throughput for multiple flows (on average 10 Mbps for each of the 10 flows), 100 Mbps throughput for single flow, and 0-2 ms RTT.
  * On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 1 10800 bbr 1 1 0` to generate 10 bbr flows at 20ms delay.
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 3 10800 bbr 1 1 0` to generate 30 bbr flows at 20ms delay.
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 5 10800 bbr 1 1 0` to generate 50 bbr flows at 20ms delay.
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 1 10800 bbr 1 1 0` to generate 10 bbr flows at 100ms delay.
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 3 10800 bbr 1 1 0` to generate 30 bbr flows at 100ms delay.
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 5 10800 bbr 1 1 0` to generate 50 bbr flows at 100ms delay.
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 1 10800 bbr 1 1 0` to generate 10 bbr flows at 200ms delay.
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 3 10800 bbr 1 1 0` to generate 30 bbr flows at 200ms delay.
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 5 10800 bbr 1 1 0` to generate 50 bbr flows at 200ms delay.
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 1 10800 cubic 1 1 0` to generate 10 cubic flows at 20ms delay.
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 3 10800 cubic 1 1 0` to generate 30 cubic flows at 20ms delay.
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 5 10800 cubic 1 1 0` to generate 50 cubic flows at 20ms delay.
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 1 10800 cubic 1 1 0` to generate 10 cubic flows at 100ms delay.
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 3 10800 cubic 1 1 0` to generate 30 cubic flows at 100ms delay.
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 5 10800 cubic 1 1 0` to generate 50 cubic flows at 100ms delay.
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 1 10800 cubic 1 1 0` to generate 10 cubic flows at 200ms delay.
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 3 10800 cubic 1 1 0` to generate 30 cubic flows at 200ms delay.
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 5 10800 cubic 1 1 0` to generate 50 cubic flows at 200ms delay.
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 1 10800 reno 1 1 0` to generate 10 reno flows at 20ms delay.
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 3 10800 reno 1 1 0` to generate 30 reno flows at 20ms delay.
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 5 10800 reno 1 1 0` to generate 50 reno flows at 20ms delay.
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 1 10800 reno 1 1 0` to generate 10 reno flows at 100ms delay.
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 3 10800 reno 1 1 0` to generate 30 reno flows at 100ms delay.
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 5 10800 reno 1 1 0` to generate 50 reno flows at 100ms delay.
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 1 10800 reno 1 1 0` to generate 10 reno flows at 200ms delay.
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 3 10800 reno 1 1 0` to generate 30 reno flows at 200ms delay.
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 5 10800 reno 1 1 0` to generate 50 reno flows at 200ms delay.


  Combined output of all the above experiment can be found at [JFI_CloudLab.csv](https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/blob/main/cloudlab-outputs/JFI_CloudLab.csv)

To validate this finding on FABRIC:

* In the Jupyter environment, select File > New > Terminal and in this terminal, run `git clone https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP`
* Open fabric-notebook subdirectory inside IMC directory.
* Run the notebook `00-reserve.ipynb` to reserve the resources. This will reserve 10 sender-reciver pair and a router. All the required dependencies or modules will be installed.
* Run the notebook `01-validate.ipynb' and confirm that you see about 24-28 Gbps sum throughput for multiple flows (on average 2.5 Gbps for each of the 10 flows), 8-17 Gbps throughput for single flow, and 0-1 ms RTT.
* Run the notebook `02-setup-core.ipynb` and confirm that you see about **10 Gbps** sum throughput for multiple flows (on average 1 Gbps for each of the 10 flows), 8-10 Gbps throughput for single flow, and 0-2 ms RTT. 
* Run the notebook `06-intra-cca-fairness.ipynb`. Set the parameters in the notebook under 'Set experiment parameters' as mentioned below to run experiments with 1000 bbr flows, 20ms delay
cca="bbr"; delay=20; test_duration=10800; num_servers=100; flows=1; interval=1; omit=0
* Run the notebook `06-intra-cca-fairness.ipynb`. Set the parameters in the notebook under 'Set experiment parameters' as mentioned below to run experiments with 3000 bbr flows, 20ms delay
cca="bbr"; delay=20; test_duration=10800; num_servers=300; flows=1; interval=1; omit=0
* Run the notebook `06-intra-cca-fairness.ipynb`. Set the parameters in the notebook under 'Set experiment parameters' as mentioned below to run experiments with 5000 bbr flows, 20ms delay
cca="bbr"; delay=20; test_duration=10800; num_servers=500; flows=1; interval=1; omit=0
* Run the notebook `06-intra-cca-fairness.ipynb`. Set the parameters in the notebook under 'Set experiment parameters' as mentioned below to run experiments with 1000 bbr flows, 100ms delay.
cca="bbr"; delay=100; test_duration=10800; num_servers=100; flows=1; interval=1; omit=0
* Run the notebook `06-intra-cca-fairness.ipynb`. Set the parameters in the notebook under 'Set experiment parameters' as mentioned below to run experiments with 3000 bbr flows, 100ms delay.
cca="bbr"; delay=100; test_duration=10800; num_servers=300; flows=1; interval=1; omit=0
* Run the notebook `06-intra-cca-fairness.ipynb`. Set the parameters in the notebook under 'Set experiment parameters' as mentioned below to run experiments with 5000 bbr flows, 100ms delay.
cca="bbr"; delay=100; test_duration=10800; num_servers=500; flows=1; interval=1; omit=0
* Run the notebook `06-intra-cca-fairness.ipynb`. Set the parameters in the notebook under 'Set experiment parameters' as mentioned below to run experiments with 1000 bbr flows, 200ms delay.
cca="bbr"; delay=200; test_duration=10800; num_servers=100; flows=1; interval=1; omit=0
* Run the notebook `06-intra-cca-fairness.ipynb`. Set the parameters in the notebook under 'Set experiment parameters' as mentioned below to run experiments with 3000 bbr flows, 200ms delay.
cca="bbr"; delay=200; test_duration=10800; num_servers=300; flows=1; interval=1; omit=0
* Run the notebook `06-intra-cca-fairness.ipynb`. Set the parameters in the notebook under 'Set experiment parameters' as mentioned below to run experiments with 5000 bbr flows, 200ms delay.
cca="bbr"; delay=200; test_duration=10800; num_servers=500; flows=1; interval=1; omit=0

* Run the notebook `06-intra-cca-fairness.ipynb`. Set the parameters in the notebook under 'Set experiment parameters' as mentioned below to run experiments with 1000 cubic flows, 20ms delay
cca="cubic"; delay=20; test_duration=10800; num_servers=100; flows=1; interval=1; omit=0
* Run the notebook `06-intra-cca-fairness.ipynb`. Set the parameters in the notebook under 'Set experiment parameters' as mentioned below to run experiments with 3000 cubic flows, 20ms delay
cca="cubic"; delay=20; test_duration=10800; num_servers=300; flows=1; interval=1; omit=0
* Run the notebook `06-intra-cca-fairness.ipynb`. Set the parameters in the notebook under 'Set experiment parameters' as mentioned below to run experiments with 5000 cubic flows, 20ms delay
cca="cubic"; delay=20; test_duration=10800; num_servers=500; flows=1; interval=1; omit=0
* Run the notebook `06-intra-cca-fairness.ipynb`. Set the parameters in the notebook under 'Set experiment parameters' as mentioned below to run experiments with 1000 cubic flows, 100ms delay.
cca="cubic"; delay=100; test_duration=10800; num_servers=100; flows=1; interval=1; omit=0
* Run the notebook `06-intra-cca-fairness.ipynb`. Set the parameters in the notebook under 'Set experiment parameters' as mentioned below to run experiments with 3000 cubic flows, 100ms delay.
cca="cubic"; delay=100; test_duration=10800; num_servers=300; flows=1; interval=1; omit=0
* Run the notebook `06-intra-cca-fairness.ipynb`. Set the parameters in the notebook under 'Set experiment parameters' as mentioned below to run experiments with 5000 cubic flows, 100ms delay.
cca="cubic"; delay=100; test_duration=10800; num_servers=500; flows=1; interval=1; omit=0
* Run the notebook `06-intra-cca-fairness.ipynb`. Set the parameters in the notebook under 'Set experiment parameters' as mentioned below to run experiments with 1000 cubic flows, 200ms delay.
cca="cubic"; delay=200; test_duration=10800; num_servers=100; flows=1; interval=1; omit=0
* Run the notebook `06-intra-cca-fairness.ipynb`. Set the parameters in the notebook under 'Set experiment parameters' as mentioned below to run experiments with 3000 cubic flows, 200ms delay.
cca="cubic"; delay=200; test_duration=10800; num_servers=300; flows=1; interval=1; omit=0
* Run the notebook `06-intra-cca-fairness.ipynb`. Set the parameters in the notebook under 'Set experiment parameters' as mentioned below to run experiments with 5000 cubic flows, 200ms delay.
cca="cubic"; delay=200; test_duration=10800; num_servers=500; flows=1; interval=1; omit=0

* Run the notebook `06-intra-cca-fairness.ipynb`. Set the parameters in the notebook under 'Set experiment parameters' as mentioned below to run experiments with 1000 reno flows, 20ms delay
cca="reno"; delay=20; test_duration=10800; num_servers=100; flows=1; interval=1; omit=0
* Run the notebook `06-intra-cca-fairness.ipynb`. Set the parameters in the notebook under 'Set experiment parameters' as mentioned below to run experiments with 3000 reno flows, 20ms delay
cca="reno"; delay=20; test_duration=10800; num_servers=300; flows=1; interval=1; omit=0
* Run the notebook `06-intra-cca-fairness.ipynb`. Set the parameters in the notebook under 'Set experiment parameters' as mentioned below to run experiments with 5000 reno flows, 20ms delay
cca="reno"; delay=20; test_duration=10800; num_servers=500; flows=1; interval=1; omit=0
* Run the notebook `06-intra-cca-fairness.ipynb`. Set the parameters in the notebook under 'Set experiment parameters' as mentioned below to run experiments with 1000 reno flows, 100ms delay.
cca="reno"; delay=100; test_duration=10800; num_servers=100; flows=1; interval=1; omit=0
* Run the notebook `06-intra-cca-fairness.ipynb`. Set the parameters in the notebook under 'Set experiment parameters' as mentioned below to run experiments with 3000 reno flows, 100ms delay.
cca="reno"; delay=100; test_duration=10800; num_servers=300; flows=1; interval=1; omit=0
* Run the notebook `06-intra-cca-fairness.ipynb`. Set the parameters in the notebook under 'Set experiment parameters' as mentioned below to run experiments with 5000 reno flows, 100ms delay.
cca="reno"; delay=100; test_duration=10800; num_servers=500; flows=1; interval=1; omit=0
* Run the notebook `06-intra-cca-fairness.ipynb`. Set the parameters in the notebook under 'Set experiment parameters' as mentioned below to run experiments with 1000 reno flows, 200ms delay.
cca="reno"; delay=200; test_duration=10800; num_servers=100; flows=1; interval=1; omit=0
* Run the notebook `06-intra-cca-fairness.ipynb`. Set the parameters in the notebook under 'Set experiment parameters' as mentioned below to run experiments with 3000 reno flows, 200ms delay.
cca="reno"; delay=200; test_duration=10800; num_servers=300; flows=1; interval=1; omit=0
* Run the notebook `06-intra-cca-fairness.ipynb`. Set the parameters in the notebook under 'Set experiment parameters' as mentioned below to run experiments with 5000 reno flows, 200ms delay.
cca="reno"; delay=200; test_duration=10800; num_servers=500; flows=1; interval=1; omit=0

* Run the notebook `04-setup-edge.ipynb` and confirm that you see about **100 Mbps** sum throughput for multiple flows (on average 10 Mbps for each of the 10 flows), 100 Mbps throughput for single flow, and 0-2 ms RTT.
* Run the notebook `06-intra-cca-fairness.ipynb`. Set the parameters in the notebook under 'Set experiment parameters' as mentioned below to run experiments with 10 bbr flows, 20ms delay
cca="bbr"; delay=20; test_duration=10800; num_servers=1; flows=1; interval=1; omit=0
* Run the notebook `06-intra-cca-fairness.ipynb`. Set the parameters in the notebook under 'Set experiment parameters' as mentioned below to run experiments with 30 bbr flows, 20ms delay
cca="bbr"; delay=20; test_duration=10800; num_servers=3; flows=1; interval=1; omit=0
* Run the notebook `06-intra-cca-fairness.ipynb`. Set the parameters in the notebook under 'Set experiment parameters' as mentioned below to run experiments with 50 bbr flows, 20ms delay
cca="bbr"; delay=20; test_duration=10800; num_servers=5; flows=1; interval=1; omit=0
* Run the notebook `06-intra-cca-fairness.ipynb`. Set the parameters in the notebook under 'Set experiment parameters' as mentioned below to run experiments with 10 bbr flows, 100ms delay.
cca="bbr"; delay=100; test_duration=10800; num_servers=1; flows=1; interval=1; omit=0
* Run the notebook `06-intra-cca-fairness.ipynb`. Set the parameters in the notebook under 'Set experiment parameters' as mentioned below to run experiments with 30 bbr flows, 100ms delay.
cca="bbr"; delay=100; test_duration=10800; num_servers=3; flows=1; interval=1; omit=0
* Run the notebook `06-intra-cca-fairness.ipynb`. Set the parameters in the notebook under 'Set experiment parameters' as mentioned below to run experiments with 50 bbr flows, 100ms delay.
cca="bbr"; delay=100; test_duration=10800; num_servers=5; flows=1; interval=1; omit=0
* Run the notebook `06-intra-cca-fairness.ipynb`. Set the parameters in the notebook under 'Set experiment parameters' as mentioned below to run experiments with 10 bbr flows, 200ms delay.
cca="bbr"; delay=200; test_duration=10800; num_servers=1; flows=1; interval=1; omit=0
* Run the notebook `06-intra-cca-fairness.ipynb`. Set the parameters in the notebook under 'Set experiment parameters' as mentioned below to run experiments with 30 bbr flows, 200ms delay.
cca="bbr"; delay=200; test_duration=10800; num_servers=3; flows=1; interval=1; omit=0
* Run the notebook `06-intra-cca-fairness.ipynb`. Set the parameters in the notebook under 'Set experiment parameters' as mentioned below to run experiments with 50 bbr flows, 200ms delay.
cca="bbr"; delay=200; test_duration=10800; num_servers=5; flows=1; interval=1; omit=0

* Run the notebook `06-intra-cca-fairness.ipynb`. Set the parameters in the notebook under 'Set experiment parameters' as mentioned below to run experiments with 10 cubic flows, 20ms delay
cca="cubic"; delay=20; test_duration=10800; num_servers=1; flows=1; interval=1; omit=0
* Run the notebook `06-intra-cca-fairness.ipynb`. Set the parameters in the notebook under 'Set experiment parameters' as mentioned below to run experiments with 30 cubic flows, 20ms delay
cca="cubic"; delay=20; test_duration=10800; num_servers=3; flows=1; interval=1; omit=0
* Run the notebook `06-intra-cca-fairness.ipynb`. Set the parameters in the notebook under 'Set experiment parameters' as mentioned below to run experiments with 50 cubic flows, 20ms delay
cca="cubic"; delay=20; test_duration=10800; num_servers=5; flows=1; interval=1; omit=0
* Run the notebook `06-intra-cca-fairness.ipynb`. Set the parameters in the notebook under 'Set experiment parameters' as mentioned below to run experiments with 10 cubic flows, 100ms delay.
cca="cubic"; delay=100; test_duration=10800; num_servers=1; flows=1; interval=1; omit=0
* Run the notebook `06-intra-cca-fairness.ipynb`. Set the parameters in the notebook under 'Set experiment parameters' as mentioned below to run experiments with 30 cubic flows, 100ms delay.
cca="cubic"; delay=100; test_duration=10800; num_servers=3; flows=1; interval=1; omit=0
* Run the notebook `06-intra-cca-fairness.ipynb`. Set the parameters in the notebook under 'Set experiment parameters' as mentioned below to run experiments with 50 cubic flows, 100ms delay.
cca="cubic"; delay=100; test_duration=10800; num_servers=5; flows=1; interval=1; omit=0
* Run the notebook `06-intra-cca-fairness.ipynb`. Set the parameters in the notebook under 'Set experiment parameters' as mentioned below to run experiments with 10 cubic flows, 200ms delay.
cca="cubic"; delay=200; test_duration=10800; num_servers=1; flows=1; interval=1; omit=0
* Run the notebook `06-intra-cca-fairness.ipynb`. Set the parameters in the notebook under 'Set experiment parameters' as mentioned below to run experiments with 30 cubic flows, 200ms delay.
cca="cubic"; delay=200; test_duration=10800; num_servers=3; flows=1; interval=1; omit=0
* Run the notebook `06-intra-cca-fairness.ipynb`. Set the parameters in the notebook under 'Set experiment parameters' as mentioned below to run experiments with 50 cubic flows, 200ms delay.
cca="cubic"; delay=200; test_duration=10800; num_servers=5; flows=1; interval=1; omit=0

* Run the notebook `06-intra-cca-fairness.ipynb`. Set the parameters in the notebook under 'Set experiment parameters' as mentioned below to run experiments with 10 reno flows, 20ms delay
cca="reno"; delay=20; test_duration=10800; num_servers=1; flows=1; interval=1; omit=0
* Run the notebook `06-intra-cca-fairness.ipynb`. Set the parameters in the notebook under 'Set experiment parameters' as mentioned below to run experiments with 30 reno flows, 20ms delay
cca="reno"; delay=20; test_duration=10800; num_servers=3; flows=1; interval=1; omit=0
* Run the notebook `06-intra-cca-fairness.ipynb`. Set the parameters in the notebook under 'Set experiment parameters' as mentioned below to run experiments with 50 reno flows, 20ms delay
cca="reno"; delay=20; test_duration=10800; num_servers=5; flows=1; interval=1; omit=0
* Run the notebook `06-intra-cca-fairness.ipynb`. Set the parameters in the notebook under 'Set experiment parameters' as mentioned below to run experiments with 10 reno flows, 100ms delay.
cca="reno"; delay=100; test_duration=10800; num_servers=1; flows=1; interval=1; omit=0
* Run the notebook `06-intra-cca-fairness.ipynb`. Set the parameters in the notebook under 'Set experiment parameters' as mentioned below to run experiments with 30 reno flows, 100ms delay.
cca="reno"; delay=100; test_duration=10800; num_servers=3; flows=1; interval=1; omit=0
* Run the notebook `06-intra-cca-fairness.ipynb`. Set the parameters in the notebook under 'Set experiment parameters' as mentioned below to run experiments with 50 reno flows, 100ms delay.
cca="reno"; delay=100; test_duration=10800; num_servers=5; flows=1; interval=1; omit=0
* Run the notebook `06-intra-cca-fairness.ipynb`. Set the parameters in the notebook under 'Set experiment parameters' as mentioned below to run experiments with 10 reno flows, 200ms delay.
cca="reno"; delay=200; test_duration=10800; num_servers=1; flows=1; interval=1; omit=0
* Run the notebook `06-intra-cca-fairness.ipynb`. Set the parameters in the notebook under 'Set experiment parameters' as mentioned below to run experiments with 30 reno flows, 200ms delay.
cca="reno"; delay=200; test_duration=10800; num_servers=3; flows=1; interval=1; omit=0
* Run the notebook `06-intra-cca-fairness.ipynb`. Set the parameters in the notebook under 'Set experiment parameters' as mentioned below to run experiments with 50 reno flows, 200ms delay.
cca="reno"; delay=200; test_duration=10800; num_servers=5; flows=1; interval=1; omit=0

 Combined output of all the above experiment can be found at [JFI_FABRIC.csv](https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/blob/main/fabric-outputs/Plots/FABRIC-results/JFI_FABRIC.csv)


Discussion: 
As per original paper:
1. NewReno & Cubic continue to show high intra-CCA fairness in CoreScale with a JFI > 0.99, as expected from past research.
2. BBR surprisingly shows intra-CCA unfairness in CoreScale, with JFIs as low as 0.4, which is not expected from past research. Milder unfairness also occurs when more than 10 flows compete in EdgeScale, with JFI’s as low as 0.7.
   <img width="441" alt="image" src="https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/assets/91571551/38fb619e-5abf-42a7-abe6-c35e918497e9">

As per experiment on CloudLab:
1. NewReno and Cubic show high intra-CCA fairness in CoreScale and EdgeScale with a JFI > 0.95
2. BBR is found more fair to other BBR flows than the original paper.
Reno:
<img width="710" alt="image" src="https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/assets/91571551/c5ca976e-443e-45a4-af20-71b08aadef83">
<img width="710" alt="image" src="https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/assets/91571551/e7855c24-8848-46e6-b616-430d7802eff1">

Cubic:
<img width="710" alt="image" src="https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/assets/91571551/e4b80750-958e-47e3-8f21-5dd0bd134a7b">
<img width="710" alt="image" src="https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/assets/91571551/8a175c18-b771-48aa-976c-2e28582bef2f">

BBR:
<img width="710" alt="image" src="https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/assets/91571551/1f03e991-411a-4b9d-a976-93dc73b4f10c">
<img width="710" alt="image" src="https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/assets/91571551/77031404-56ef-401d-99c8-502f5126605b">

Data source of all above plots is [JFI_CloudLab.csv](https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/blob/main/cloudlab-outputs/JFI_CloudLab.csv)
All the above plots can be found at [JFI_plot_CloudLab.pdf](https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/blob/main/cloudlab-outputs/Plots/Results/JFI_plot_CloudLab.pdf)


As per experiment on FABRIC:
1. NewReno and Cubic show high intra-CCA fairness in CoreScale and EdgeScale with a JFI > 0.91
2. BBR is found more fair to other BBR flows than the original paper.
Reno:
<img width="710" alt="image" src="https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/assets/91571551/5a061002-a887-4c07-aaca-6ce06c2b643e">
<img width="710" alt="image" src="https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/assets/91571551/0c1eb469-367f-4ee1-8508-8166a51cc104">

Cubic:
<img width="710" alt="image" src="https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/assets/91571551/2c04b6e0-c9c6-45e3-ab5e-d5b062303b3b">
<img width="710" alt="image" src="https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/assets/91571551/1eb52592-93c6-47df-a426-4013f8a24f55">

BBR:
<img width="710" alt="image" src="https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/assets/91571551/8f12b412-8c10-44b0-8004-cbecb1dd25f8">
<img width="710" alt="image" src="https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/assets/91571551/28450fc8-a572-4ab4-b0f5-178917c97826">


Data source of all above plots is [JFI_FABRIC.csv](https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/blob/main/fabric-outputs/JFI_FABRIC.csv)
All the above plots can be found at [JFI_Plots_FABRIC.pdf](https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/blob/main/fabric-outputs/Plots/FABRIC-results/JFI_plot_FABRIC.pdf)



## Finding 3

> Cubic achieves 70 to 80% of total throughput when competing with an equal number of NewReno flows at CoreScale, while BBR is highly unfair to loss-based CCA, i.e., NewReno and Cubic. These results are in line with past research in the edge setting.

To validate this finding on CloudLab:

* Open the CloudLab profile. Leave parameters at their default settings, and reserve resources at CloudLab Utah. Wait for resources to come up and for startup scripts to be complete. Open an SSH terminal at the router.

* On the router: run bash /local/repository/cloudlab-scripts/validate.sh and confirm that you see about 24-25 Gbps sum throughput for multiple flows (on average 2.5 Gbps for each of the 10 flows), 8-10 Gbps throughput for single flow, and 0-1 ms RTT.

* On the router: run bash /local/repository/cloudlab-scripts/setup-core.sh and confirm that you see about 10 Gbps sum throughput for multiple flows (on average 1 Gbps for each of the 10 flows), 7-10 Gbps throughput for single flow, and 0-2 ms RTT. 

* To validate this: "Cubic achieves 70 to 80% of total throughput when competing with an equal number of NewReno flows at CoreScale", On the router run: bash generate-flows.sh 20 10000000 2 10 1800 reno 10 1 cubic

Example output from running the command is 
count of flows of reno is 500
sum of Bandwidth of reno is 1833615 Kbits/sec
count of flows of cubic is 500
sum of Bandwidth of cubic is 8064566 Kbits/sec

* To validate this: "BBR is highly unfair to loss-based CCA, i.e., NewReno and Cubic", On the router run: bash generate-flows.sh 20 10000000 3 10 1800 reno 10 1 bbr

Example output from running the command is 
count of flows of reno is 499
sum of Bandwidth of reno is 5861246 Kbits/sec
count of flows of bbr is 1
sum of Bandwidth of bbr is 93807 Kbits/sec


To validate this finding on FABRIC:

As per the original paper, we have 
1) Cubic achieves 70 to 80% of total throughput when competing with an equal number of NewReno flows at CoreScale 
2) BBR is highly unfair to loss-based CCA, i.e., NewReno and Cubic. A single BBR flow takes 40% of the total throughput when competing with thousands of NewReno or Cubic flows. 

<img width="394" alt="Screenshot 2023-08-21 at 9 28 02 AM" src="https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/assets/10760836/1077ba81-6f8c-470f-b45f-b626933fc6bf">

<img width="816" alt="Screenshot 2023-08-21 at 9 45 31 AM" src="https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/assets/10760836/0b17c093-2bb2-4cf1-b9a3-b78eeee515bc">

As per our experiment on CloudLab, we have 
1)  Cubic achieves 70 to 80% of total throughput when competing with an equal number of NewReno flows at CoreScale : which is same as the finding of the paper

![Cubic Vs Reno _ 20ms RTT](https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/assets/10760836/84804668-7965-46f7-afce-ff7dd4cd2f3f)

![Cubic Vs Reno _ 100ms RTT](https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/assets/10760836/7a81c67a-4a01-47cd-aab0-f73e84fc3ab3)

![Cubic Vs Reno _ 200ms RTT](https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/assets/10760836/e4876c45-e82b-4e0d-8c82-a6ee8f11ad3b)

2) BBR seems to be highly FAIR when competing with Loss-based CCA. A single BBR flow takes only 1% of the total throughput when competing with thousands of NewReno or Cubic flows. 

Discussion: 

As per the original paper, we have 
1) Cubic achieves 70 to 80% of total throughput when competing with an equal number of NewReno flows at CoreScale 
2) BBR is highly unfair to loss-based CCA, i.e., NewReno and Cubic. A single BBR flow takes 40% of the total throughput when competing with thousands of NewReno or Cubic flows. 

<img width="394" alt="Screenshot 2023-08-21 at 9 28 02 AM" src="https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/assets/10760836/1077ba81-6f8c-470f-b45f-b626933fc6bf">

<img width="816" alt="Screenshot 2023-08-21 at 9 45 31 AM" src="https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/assets/10760836/0b17c093-2bb2-4cf1-b9a3-b78eeee515bc">

As per our experiment on CloudLab, we have 
1)  Cubic achieves 70 to 80% of total throughput when competing with an equal number of NewReno flows at CoreScale : which is same as the finding of the paper

![Cubic Vs Reno _ 20ms RTT](https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/assets/10760836/84804668-7965-46f7-afce-ff7dd4cd2f3f)

![Cubic Vs Reno _ 100ms RTT](https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/assets/10760836/7a81c67a-4a01-47cd-aab0-f73e84fc3ab3)

![Cubic Vs Reno _ 200ms RTT](https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/assets/10760836/e4876c45-e82b-4e0d-8c82-a6ee8f11ad3b)

2) BBR seems to be highly FAIR when competing with Loss-based CCA. A single BBR flow takes only 1% of the total throughput when competing with thousands of NewReno or Cubic flows.

count of flows of reno is 999
sum of Bandwidth of reno is 9409565 Kbits/sec
count of flows of bbr is 1
sum of Bandwidth of bbr is 90762 Kbits/sec
BBR Throughput share = BBRTP/(RENO+BBR) = 0.00955356589 = 1% 


## Extension to intermediate settings

### Finding 1
> The Mathis model for TCP NewReno throughput is valid at CoreScale only if the congestion event rate (p) and model parameter C are calculated using the CWND-halving rate, rather than the conventional packet loss rate that is typically used for EdgeScale.

To validate this finding on CloudLab:

* Open the [CloudLab profile](https://www.cloudlab.us/p/nyunetworks/imc-revisiting). Leave parameters at their default settings, and reserve resources at CloudLab Utah. Wait for resources to come up and for startup scripts to be complete. Open an SSH terminal at the router.
* On the router: run `bash /local/repository/cloudlab-scripts/validate.sh` and confirm that you see about 24-25 Gbps sum throughput for multiple flows (on average 2.5 Gbps for each of the 10 flows), 5-8 Gbps throughput for single flow, and 0-1 ms RTT. [Sample output](https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/blob/main/cloudlab-outputs/validate_output.txt)
* * Run the notebook `03-setup-intermediate.ipynb` and confirm that you see about **1 Gbps** sum throughput for multiple flows (on average 100 Mbps for each of the 10 flows), 1 Gbps throughput for single flow, and 0-2 ms RTT.[Sample output](https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/blob/main/cloudlab-outputs/setup_intermediate_output.txt)
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 10 10800 reno 1 0.01 0` to generate 100 flows.
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 30 10800 reno 1 0.01 0` to generate 300 flows.
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 50 10800 reno 1 0.01 0` to generate 500 flows.

The combined output of all the experiments can be found at [C_CloudLab.csv](https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/blob/main/cloudlab-outputs/C_CloudLab.csv)
Linear regression plots are available at [Linear_Regression_Plots](https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/tree/main/cloudlab-outputs/Plots/Linear-Regression-plots)

To validate this finding on FABRIC:

* In the Jupyter environment, select File > New > Terminal and in this terminal, run `git clone https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP`
* Open fabric-notebook subdirectory inside IMC directory.
* Run the notebook `00-reserve.ipynb` to reserve the resources. This will reserve 10 sender-reciver pair and a router. All the required dependencies or modules will be installed.
* Run the notebook `01-validate.ipynb' and confirm that you see about 24-28 Gbps sum throughput for multiple flows (on average 2.5 Gbps for each of the 10 flows), 8-17 Gbps throughput for single flow, and 0-1 ms RTT.
* Run the notebook `03-setup-intermediate.ipynb` and confirm that you see about **1 Gbps** sum throughput for multiple flows (on average 100 Mbps for each of the 10 flows), 1 Gbps throughput for single flow, and 0-2 ms RTT.
* Run the notebook `05-get-mathis-constant.ipynb`. Set the parameters in the notebook under 'Set experiment parameters' as mentioned below to run experiments with 100 reno flows.
cca="reno"; delay=20; test_duration=10800; num_servers=10; flows=1; interval=0.01; omit=0
* Run the notebook `05-get-mathis-constant.ipynb`. Set the parameters in the notebook under 'Set experiment parameters' as mentioned below to run experiments with 300 reno flows.
cca="reno"; delay=20; test_duration=10800; num_servers=30; flows=1; interval=0.01; omit=0
* Run the notebook `05-get-mathis-constant.ipynb`. Set the parameters in the notebook under 'Set experiment parameters' as mentioned below to run experiments with 500 reno flows.
cca="reno"; delay=20; test_duration=10800; num_servers=50; flows=1; interval=0.01; omit=0

The output of all the above experiments can be found at [C_FABRIC.csv](https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/blob/main/fabric-outputs/C_FABRIC.csv)
All the regression plots are available at [Linear-regression-plots](https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/tree/main/fabric-outputs/Plots/Linear-Regression-Plots)

Discussion:

Experiment results from CloudLab:
Our experiment validates the original findings and CWND halving rate results in flow count-independent constant in IntermediateScale.
<img width="640" alt="image" src="https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/assets/91571551/1907477e-8f09-48e5-9214-de8c65cd1492">

Our experiment shows that the ratio between packet loss to CWND halving rate is almost constant at IntermediateScale.
<img width="600" alt="image" src="https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/assets/91571551/b51961e0-9c4a-41e1-aa8e-c109b01fda83">

Experiment results from FABRIC:
Our experiment validates the original findings and CWND halving rate results in flow count-independent constant in IntermediateScale.
<img width="600" alt="image" src="https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/assets/91571551/11070c2b-6cf1-47eb-af37-793939f2367d">

Our experiment shows that the ratio between packet loss to CWND halving rate is almost constant at IntermediateScale.
<img width="600" alt="image" src="https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/assets/91571551/f3e6018d-82a0-4df4-a581-7053c64ece57">




## Finding 2

> NewReno and Cubic show high intra-CCA fairness in CoreScale, in line with past research. BBR shows poor intra-CCA fairness in CoreScale, contradicting previous research in the edge setting.

To validate this finding on CloudLab:


* Open the [CloudLab profile](https://www.cloudlab.us/p/nyunetworks/imc-revisiting). Leave parameters at their default settings, and reserve resources at CloudLab Utah. Wait for resources to come up and for startup scripts to be complete. Open an SSH terminal at the router.
* On the router: run `bash /local/repository/cloudlab-scripts/validate.sh` and confirm that you see about 24-25 Gbps sum throughput for multiple flows (on average 2.5 Gbps for each of the 10 flows), 5-8 Gbps throughput for single flow, and 0-1 ms RTT. [Sample output](https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/blob/main/cloudlab-outputs/validate_output.txt)
* On the router: run `bash /local/repository/cloudlab-scripts/setup-intremediate.sh` and confirm that you see about **1 Gbps** sum throughput for multiple flows (on average 100 Mbps for each of the 10 flows), 1 Gbps throughput for single flow, and 0-2 ms RTT.
To validate this finding on CloudLab:
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 10 10800 bbr 1 1 0` to generate 100 bbr flows at 20ms delay.
  'jfi.csv' file is created (if there is none otherwise append the current result in new line). It has cca, duration of expt(sec), base RTT(ms)', total bandwidth(Kbps), sum of square of bandwidth, flow count and JFI.
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 30 10800 bbr 1 1 0` to generate 300 bbr flows at 20ms delay.
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 50 10800 bbr 1 1 0` to generate 500 bbr flows at 20ms delay.
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 10 10800 bbr 1 1 0` to generate 100 bbr flows at 100ms delay.
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 30 10800 bbr 1 1 0` to generate 300 bbr flows at 100ms delay.
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 50 10800 bbr 1 1 0` to generate 500 bbr flows at 100ms delay.
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 10 10800 bbr 1 1 0` to generate 100 bbr flows at 200ms delay.
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 30 10800 bbr 1 1 0` to generate 300 bbr flows at 200ms delay.
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 50 10800 bbr 1 1 0` to generate 500 bbr flows at 200ms delay.
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 10 10800 cubic 1 1 0` to generate 100 cubic flows at 20ms delay.
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 30 10800 cubic 1 1 0` to generate 300 cubic flows at 20ms delay.
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 50 10800 cubic 1 1 0` to generate 500 cubic flows at 20ms delay.
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 10 10800 cubic 1 1 0` to generate 100 cubic flows at 100ms delay.
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 30 10800 cubic 1 1 0` to generate 300 cubic flows at 100ms delay.
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 50 10800 cubic 1 1 0` to generate 500 cubic flows at 100ms delay.
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 10 10800 cubic 1 1 0` to generate 100 cubic flows at 200ms delay.
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 30 10800 cubic 1 1 0` to generate 300 cubic flows at 200ms delay.
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 50 10800 cubic 1 1 0` to generate 500 cubic flows at 200ms delay.
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 10 10800 reno 1 1 0` to generate 100 reno flows at 20ms delay.
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 30 10800 reno 1 1 0` to generate 300 reno flows at 20ms delay.
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 50 10800 reno 1 1 0` to generate 500 reno flows at 20ms delay.
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 10 10800 reno 1 1 0` to generate 100 reno flows at 100ms delay.
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 30 10800 reno 1 1 0` to generate 300 reno flows at 100ms delay.
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 50 10800 reno 1 1 0` to generate 500 reno flows at 100ms delay.
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 10 10800 reno 1 1 0` to generate 100 reno flows at 200ms delay.
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 30 10800 reno 1 1 0` to generate 300 reno flows at 200ms delay.
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 1000000 1 50 10800 reno 1 1 0` to generate 500 reno flows at 200ms delay.

To validate this finding on FABRIC:

* In the Jupyter environment, select File > New > Terminal and in this terminal, run `https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP`
* Open fabric-notebook subdirectory inside IMC directory.
* Run the notebook `00-reserve.ipynb` to reserve the resources. This will reserve 10 sender-reciver pair and a router. All the required dependencies or modules will be installed.
* Run the notebook `01-validate.ipynb' and confirm that you see about 24-28 Gbps sum throughput for multiple flows (on average 2.5 Gbps for each of the 10 flows), 8-17 Gbps throughput for single flow, and 0-1 ms RTT.
* Run the notebook `02-setup-intermediate.ipynb` and confirm that you see about **1 Gbps** sum throughput for multiple flows (on average 100 Mbps for each of the 10 flows), 1 Gbps throughput for single flow, and 0-2 ms RTT. 
* * Run the notebook `06-intra-cca-fairness.ipynb`. Set the parameters in the notebook under 'Set experiment parameters' as mentioned below to run experiments with 100 bbr flows, 20ms delay
cca="bbr"; delay=20; test_duration=10800; num_servers=10; flows=1; interval=1; omit=0
* Run the notebook `06-intra-cca-fairness.ipynb`. Set the parameters in the notebook under 'Set experiment parameters' as mentioned below to run experiments with 300 bbr flows, 20ms delay
cca="bbr"; delay=20; test_duration=10800; num_servers=30; flows=1; interval=1; omit=0
* Run the notebook `06-intra-cca-fairness.ipynb`. Set the parameters in the notebook under 'Set experiment parameters' as mentioned below to run experiments with 500 bbr flows, 20ms delay
cca="bbr"; delay=20; test_duration=10800; num_servers=50; flows=1; interval=1; omit=0
* Run the notebook `06-intra-cca-fairness.ipynb`. Set the parameters in the notebook under 'Set experiment parameters' as mentioned below to run experiments with 100 bbr flows, 100ms delay.
cca="bbr"; delay=100; test_duration=10800; num_servers=10; flows=1; interval=1; omit=0
* Run the notebook `06-intra-cca-fairness.ipynb`. Set the parameters in the notebook under 'Set experiment parameters' as mentioned below to run experiments with 300 bbr flows, 100ms delay.
cca="bbr"; delay=100; test_duration=10800; num_servers=30; flows=1; interval=1; omit=0
* Run the notebook `06-intra-cca-fairness.ipynb`. Set the parameters in the notebook under 'Set experiment parameters' as mentioned below to run experiments with 500 bbr flows, 100ms delay.
cca="bbr"; delay=100; test_duration=10800; num_servers=50; flows=1; interval=1; omit=0
* Run the notebook `06-intra-cca-fairness.ipynb`. Set the parameters in the notebook under 'Set experiment parameters' as mentioned below to run experiments with 100 bbr flows, 200ms delay.
cca="bbr"; delay=200; test_duration=10800; num_servers=10; flows=1; interval=1; omit=0
* Run the notebook `06-intra-cca-fairness.ipynb`. Set the parameters in the notebook under 'Set experiment parameters' as mentioned below to run experiments with 300 bbr flows, 200ms delay.
cca="bbr"; delay=200; test_duration=10800; num_servers=30; flows=1; interval=1; omit=0
* Run the notebook `06-intra-cca-fairness.ipynb`. Set the parameters in the notebook under 'Set experiment parameters' as mentioned below to run experiments with 500 bbr flows, 200ms delay.
cca="bbr"; delay=200; test_duration=10800; num_servers=50; flows=1; interval=1; omit=0

* Run the notebook `06-intra-cca-fairness.ipynb`. Set the parameters in the notebook under 'Set experiment parameters' as mentioned below to run experiments with 100 cubic flows, 20ms delay
cca="cubic"; delay=20; test_duration=10800; num_servers=10; flows=1; interval=1; omit=0
* Run the notebook `06-intra-cca-fairness.ipynb`. Set the parameters in the notebook under 'Set experiment parameters' as mentioned below to run experiments with 300 cubic flows, 20ms delay
cca="cubic"; delay=20; test_duration=10800; num_servers=30; flows=1; interval=1; omit=0
* Run the notebook `06-intra-cca-fairness.ipynb`. Set the parameters in the notebook under 'Set experiment parameters' as mentioned below to run experiments with 500 cubic flows, 20ms delay
cca="cubic"; delay=20; test_duration=10800; num_servers=50; flows=1; interval=1; omit=0
* Run the notebook `06-intra-cca-fairness.ipynb`. Set the parameters in the notebook under 'Set experiment parameters' as mentioned below to run experiments with 100 cubic flows, 100ms delay.
cca="cubic"; delay=100; test_duration=10800; num_servers=10; flows=1; interval=1; omit=0
* Run the notebook `06-intra-cca-fairness.ipynb`. Set the parameters in the notebook under 'Set experiment parameters' as mentioned below to run experiments with 300 cubic flows, 100ms delay.
cca="cubic"; delay=100; test_duration=10800; num_servers=30; flows=1; interval=1; omit=0
* Run the notebook `06-intra-cca-fairness.ipynb`. Set the parameters in the notebook under 'Set experiment parameters' as mentioned below to run experiments with 500 cubic flows, 100ms delay.
cca="cubic"; delay=100; test_duration=10800; num_servers=50; flows=1; interval=1; omit=0
* Run the notebook `06-intra-cca-fairness.ipynb`. Set the parameters in the notebook under 'Set experiment parameters' as mentioned below to run experiments with 100 cubic flows, 200ms delay.
cca="cubic"; delay=200; test_duration=10800; num_servers=10; flows=1; interval=1; omit=0
* Run the notebook `06-intra-cca-fairness.ipynb`. Set the parameters in the notebook under 'Set experiment parameters' as mentioned below to run experiments with 300 cubic flows, 200ms delay.
cca="cubic"; delay=200; test_duration=10800; num_servers=30; flows=1; interval=1; omit=0
* Run the notebook `06-intra-cca-fairness.ipynb`. Set the parameters in the notebook under 'Set experiment parameters' as mentioned below to run experiments with 500 cubic flows, 200ms delay.
cca="cubic"; delay=200; test_duration=10800; num_servers=50; flows=1; interval=1; omit=0

* Run the notebook `06-intra-cca-fairness.ipynb`. Set the parameters in the notebook under 'Set experiment parameters' as mentioned below to run experiments with 100 reno flows, 20ms delay
cca="reno"; delay=20; test_duration=10800; num_servers=10; flows=1; interval=1; omit=0
* Run the notebook `06-intra-cca-fairness.ipynb`. Set the parameters in the notebook under 'Set experiment parameters' as mentioned below to run experiments with 300 reno flows, 20ms delay
cca="reno"; delay=20; test_duration=10800; num_servers=30; flows=1; interval=1; omit=0
* Run the notebook `06-intra-cca-fairness.ipynb`. Set the parameters in the notebook under 'Set experiment parameters' as mentioned below to run experiments with 500 reno flows, 20ms delay
cca="reno"; delay=20; test_duration=10800; num_servers=50; flows=1; interval=1; omit=0
* Run the notebook `06-intra-cca-fairness.ipynb`. Set the parameters in the notebook under 'Set experiment parameters' as mentioned below to run experiments with 100 reno flows, 100ms delay.
cca="reno"; delay=100; test_duration=10800; num_servers=10; flows=1; interval=1; omit=0
* Run the notebook `06-intra-cca-fairness.ipynb`. Set the parameters in the notebook under 'Set experiment parameters' as mentioned below to run experiments with 300 reno flows, 100ms delay.
cca="reno"; delay=100; test_duration=10800; num_servers=30; flows=1; interval=1; omit=0
* Run the notebook `06-intra-cca-fairness.ipynb`. Set the parameters in the notebook under 'Set experiment parameters' as mentioned below to run experiments with 500 reno flows, 100ms delay.
cca="reno"; delay=100; test_duration=10800; num_servers=50; flows=1; interval=1; omit=0
* Run the notebook `06-intra-cca-fairness.ipynb`. Set the parameters in the notebook under 'Set experiment parameters' as mentioned below to run experiments with 100 reno flows, 200ms delay.
cca="reno"; delay=200; test_duration=10800; num_servers=10; flows=1; interval=1; omit=0
* Run the notebook `06-intra-cca-fairness.ipynb`. Set the parameters in the notebook under 'Set experiment parameters' as mentioned below to run experiments with 300 reno flows, 200ms delay.
cca="reno"; delay=200; test_duration=10800; num_servers=30; flows=1; interval=1; omit=0
* Run the notebook `06-intra-cca-fairness.ipynb`. Set the parameters in the notebook under 'Set experiment parameters' as mentioned below to run experiments with 500 reno flows, 200ms delay.
cca="reno"; delay=200; test_duration=10800; num_servers=50; flows=1; interval=1; omit=0

Discussion:
As per original paper:
1. NewReno & Cubic continue to show high intra-CCA fairness in CoreScale with a JFI > 0.99, as expected from past research.
2. BBR surprisingly shows intra-CCA unfairness in CoreScale, with JFIs as low as 0.4, which is not expected from past research. Milder unfairness also occurs when more than 10 flows compete in EdgeScale, with JFI’s as low as 0.7.
   <img width="441" alt="image" src="https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/assets/91571551/38fb619e-5abf-42a7-abe6-c35e918497e9">

As per experiment on CloudLab:
1. NewReno and Cubic show high intra-CCA fairness in CoreScale and EdgeScale with a JFI > 0.97
2. BBR is found to be more fair than the original paper.

<img width="701" alt="image" src="https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/assets/91571551/3e218053-50a2-4381-8fc6-12fec467b1fe">
<img width="701" alt="image" src="https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/assets/91571551/aab8739f-a2d3-4084-80f5-20c15eeb1109">


<img width="701" alt="image" src="https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/assets/91571551/95b67144-a0bb-47a4-a5f2-8f8be7c8dd1f">


As per experiment on FABRIC:
1. NewReno and Cubic show high intra-CCA fairness in CoreScale and EdgeScale with a JFI > 0.93
2. BBR is found to be more fair than the original paper.
   [JFI_FABRIC_intermediate.csv](https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/blob/main/fabric-outputs/JFI_FABRIC_Intermediate.csv)

<img width="701" alt="image" src="https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/assets/91571551/6a22f2f1-06cd-4f5e-ac73-c807dd8d555c">
<img width="701" alt="image" src="https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/assets/91571551/155a2a93-da88-4aa7-b96f-8f415cb4d310">
<img width="701" alt="image" src="https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/assets/91571551/d155974c-d22e-46ff-bc2e-1628609f86e2">



Finding 3: 

> Cubic achieves 70 to 80% of total throughput when competing with an equal number of NewReno flows at CoreScale, while BBR is highly unfair to loss-based CCA, i.e., NewReno and Cubic. These results are in line with past research in the edge setting.

To validate this finding on CloudLab:
* Open the [CloudLab profile](https://www.cloudlab.us/p/nyunetworks/imc-revisiting). Leave parameters at their default settings, and reserve resources at CloudLab Utah. Wait for resources to come up and for startup scripts to be complete. Open an SSH terminal at the router.
* On the router: run `bash /local/repository/cloudlab-scripts/validate.sh` and confirm that you see about 24-25 Gbps sum throughput for multiple flows (on average 2.5 Gbps for each of the 10 flows), 8-10 Gbps throughput for single flow, and 0-1 ms RTT.
* On the router: run `bash /local/repository/cloudlab-scripts/setup-intremediate.sh` and confirm that you see about **1 Gbps** sum throughput for multiple flows (on average 100 Mbps for each of the 10 flows), 1 Gbps throughput for single flow, and 0-2 ms RTT.
* On the router: run `bash /local/repository/cloudlab-scripts/generate-flows.sh 20 10000000 3 10 1800 reno 1 1 bbr`.

* Example output from running the command is
  `count of flows of reno is 99, sum of Bandwidth of reno is 1731767 Kbits/sec, count of flows of bbr is 1, sum of Bandwidth of bbr is 37065 Kbits/sec`

Discussion:
As per the original paper: BBR is highly unfair to loss-based CCA, i.e., NewReno and Cubic. A single BBR flow takes 40% of the total throughput when competing with thousands of NewReno or Cubic flows. 

According to our results: 

<img width="897" alt="Screenshot 2023-08-23 at 10 27 32 AM" src="https://github.com/vinitaparasrampuria/IMC-Revisiting-TCP/assets/10760836/4689a5f1-7806-4b2c-b258-67400171c13b">

