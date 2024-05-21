#!/usr/bin/env python

"""
Lab 5: Setting WAN Bandwidth with Token Bucket Filter (TBF)
Experiment 1: Rate limiting on end-hosts
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

    info('*** Adding switches\n')
    s1 = net.addSwitch('s1')
    s2 = net.addSwitch('s2')

    info('*** Creating links\n')
    net.addLink(h1, s1, intfName1='h1-eth0', intfName2='s1-eth1')
    net.addLink(s1, s2, intfName1='s1-eth2', intfName2='s2-eth2')
    net.addLink(s2, h2, intfName1='s2-eth1', intfName2='h2-eth0')

    info('*** Starting network\n')
    net.start()

    # Step 1: Set bandwidth on host h1's interface
    info('*** Set bandwidth on host h1\n')
    h1.cmdPrint('sudo tc qdisc add dev h1-eth0 root tbf rate 10gbit burst 5000000 limit 15000000')

    time.sleep(2)  # Wait for the configuration to take effect

    # Step 2: Launch iPerf3 server on host h2
    info('*** Launch iPerf3 server on host h2\n')
    h2.cmdPrint('iperf3 -s &')

    # Step 3: Launch iPerf3 client on host h1 and record results
    info('*** Launch iPerf3 client on host h1 and record results\n')
    h1.cmdPrint('iperf3 -c 10.0.0.2 > res_lab5_1.txt')

    info('*** Stopping network\n')
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    emptyNet()
