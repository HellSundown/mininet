#!/usr/bin/env python

"""
Lab 10: Measuring TCP Fairness
"""

from mininet.net import Mininet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.log import setLogLevel, info
import time

def emptyNet():
    "Create an empty network and add nodes to it."

    net = Mininet(controller=Controller, waitConnected=True)

    info('*** Adding controller\n')
    net.addController('c0')

    info('*** Adding hosts\n')
    h1 = net.addHost('h1', ip='10.0.0.1')
    h2 = net.addHost('h2', ip='10.0.0.2')
    h3 = net.addHost('h3', ip='10.0.0.3')
    h4 = net.addHost('h4', ip='10.0.0.4')

    info('*** Adding switches\n')
    s1 = net.addSwitch('s1')
    s2 = net.addSwitch('s2')

    info('*** Creating links\n')
    net.addLink(h1, s1, intfName1='h1-eth0', intfName2='s1-eth3')
    net.addLink(h3, s1, intfName1='h3-eth0', intfName2='s1-eth2')
    net.addLink(h2, s2, intfName1='h2-eth0', intfName2='s2-eth3')
    net.addLink(h4, s2, intfName1='h4-eth0', intfName2='s2-eth2')
    net.addLink(s1, s2, intfName1='s1-eth1', intfName2='s2-eth1')

    info('*** Starting network\n')
    net.start()

    # Step 2: Introduce 20ms delay on switch S1's s1-eth1 interface
    info('*** Introduce delay on switch S1\n')
    s1.cmdPrint('sudo tc qdisc add dev s1-eth1 root handle 1: netem delay 20ms')

    time.sleep(2)  # Wait for the configuration to take effect

    # Step 3: Modify bandwidth of the link connecting switch S1 and switch S2
    info('*** Modify bandwidth on the link between switches S1 and S2\n')
    s1.cmdPrint('sudo tc qdisc add dev s1-eth1 parent 1: handle 2: tbf rate 10gbit burst 5000000 limit 15000000')

    time.sleep(2)  # Wait for the configuration to take effect

    # Step 3: Launch iPerf3 server on h2
    info('*** Launch iPerf3 server on h2\n')
    h2.cmdPrint('iperf3 -s &')

    # Step 4: Launch iPerf3 client on h1
    info('*** Launch iPerf3 client on h1\n')
    h1.cmdPrint('iperf3 -c 10.0.0.2')

    h1.cmdPrint("sysctl -w net.ipv4.tcp_rmem='10240 87380 52428800'")
    h1.cmdPrint("sysctl -w net.ipv4.tcp_wmem='10240 87380 52428800'")

    # Step 1: Launch iPerf3 server on h2
    info('*** Launch iPerf3 server on h2 for parallel flows\n')
    h2.cmdPrint('iperf3 -s &')

    # Step 2: Launch iPerf3 client on h1 with parallel streams and save output to JSON file
    info('*** Launch iPerf3 client on h1 with parallel streams and save output to JSON file\n')
    h1.cmdPrint('iperf3 -c 10.0.0.2 -P 8 -J > out.json')

    # Step 3: Calculate fairness index using fairness.sh
    info('*** Calculate fairness index using fairness.sh\n')
    h2.cmdPrint('fairness.sh out.json')

    # Step 4: Stop iPerf3 server on h2
    info('*** Stop iPerf3 server on h2\n')
    h2.cmdPrint('sudo pkill iperf3')

    info('*** Stopping network\n')
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    emptyNet()
