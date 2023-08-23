"""10 senders, 10 receivers, and bottleneck router in middle."""

#
# NOTE: This code was machine converted. An actual human would not
#       write code like this!
#

# Import the Portal object.
import geni.portal as portal
# Import the ProtoGENI library.
import geni.rspec.pg as pg
# Import the Emulab specific extensions.
import geni.rspec.emulab as emulab

# Create a portal object,
pc = portal.Context()

# Describe the parameter(s) this profile script can accept.
pc.defineParameter( "n", "Number of hosts on either end of dumbbell", portal.ParameterType.INTEGER, 10 )
pc.defineParameter( "v", "Use VMs?", portal.ParameterType.BOOLEAN, False)
# Optional physical type for all nodes.
pc.defineParameter("rtrtype",  "Physical node type for router",
                   portal.ParameterType.STRING, "c6525-25g",
                   longDescription="Specify a single physical node type (d6515,c6525-25g,c6525-100g,etc)")
pc.defineParameter("endtype",  "Physical node type for end hosts",
                   portal.ParameterType.STRING, "m400",
                   longDescription="Specify a single physical node type (m400,c6525-25g,c6525-100g,etc)")
pc.defineParameter( "c", "Link capacity for router", portal.ParameterType.INTEGER, 25000000 )

# Retrieve the values the user specifies during instantiation.
params = pc.bindParameters()


# Create a Request object to start building the RSpec.
request = pc.makeRequestRSpec()

# Node router
node_router = request.RawPC('router')
node_router.disk_image = 'urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU22-64-STD'
node_router.hardware_type = params.rtrtype
bs_node = node_router.Blockstore("bs_node_router", "/mydata")
bs_node.size = "0GB"
node_router.addService(pg.Execute(shell="bash", command="bash /local/repository/setup-scripts/mlnx-install.sh; bash /local/repository/setup-scripts/install.sh"))
node_router.addService(pg.Execute(shell="bash", command="sudo chmod a+r /mydata; sudo chmod a+w /mydata"))
node_router.addService(pg.Execute(shell="bash", command="bash /local/repository/setup-scripts/no-offload.sh"))

node_router.installRootKeys(True, True)
iface1 = node_router.addInterface('interface-r-send', pg.IPv4Address('10.10.1.1','255.255.255.0'))
iface2 = node_router.addInterface('interface-r-recv', pg.IPv4Address('10.10.2.1','255.255.255.0'))

# Link link-0
link_0 = request.Link('link-sender')
iface1.bandwidth = params.c
link_0.bandwidth = params.c
link_0.addInterface(iface1)

# Link link-1
link_1 = request.Link('link-receiver')
iface2.bandwidth = params.c
link_1.bandwidth = params.c
link_1.addInterface(iface2)

for i in range(params.n):
    if params.v:
        node_sender = request.XenVM('sender-' + str(i))
    else:
        node_sender = request.RawPC('sender-' + str(i))
        node_sender.hardware_type = params.endtype
    node_sender.disk_image = 'urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU18-64-STD'
    bs_node = node_sender.Blockstore("bs_node_" + str(i), "/mydata")
    bs_node.size = "0GB"
    node_sender.installRootKeys(True, True)
    node_sender.addService(pg.Execute(shell="bash", command="sudo chmod a+r /mydata; sudo chmod a+w /mydata; sudo modprobe tcp_bbr"))
    node_sender.addService(pg.Execute(shell="bash", command="bash /local/repository/setup-scripts/install.sh; bash /local/repository/endpoint-scripts/install_iperf.sh"))
    node_sender.addService(pg.Execute(shell="bash", command="bash /local/repository/setup-scripts/no-offload.sh"))
    iface0 = node_sender.addInterface('interface-send-' + str(i), pg.IPv4Address('10.10.1.1' + str(i) ,'255.255.255.0'))
    iface0.bandwidth = 10000000
    link_0.addInterface(iface0)
    

for i in range(params.n):
    if params.v:
        node_receiver = request.XenVM('receiver-' + str(i))
    else:
        node_receiver = request.RawPC('receiver-' + str(i))
        node_receiver.hardware_type = params.endtype
    node_receiver.disk_image = 'urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU18-64-STD'
    node_receiver.installRootKeys(True, True)
    node_receiver.addService(pg.Execute(shell="bash", command="sudo apt-get update; sudo apt-get -y install iperf3; sudo modprobe tcp_bbr"))
    #node_receiver.addService(pg.Execute(shell="bash", command="bash /local/repository/setup-scripts/no-offload.sh"))  
    iface0 = node_receiver.addInterface('interface-recv-' + str(i), pg.IPv4Address('10.10.2.1' + str(i),'255.255.255.0'))
    iface0.bandwidth = 10000000
    link_1.addInterface(iface0)


# Print the generated rspec
pc.printRequestRSpec(request)
