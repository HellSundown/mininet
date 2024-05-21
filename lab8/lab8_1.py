#!/usr/bin/env python

"""
Bandwidth-delay Product and TCP Buffer Size Experiment.
Output: throughput.json
"""

from mininet.net import Mininet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.log import setLogLevel, info
import time

def BDPExperiment():

    "Create a network and run BDP experiment."

    net = Mininet(controller=Controller, waitConnected=True)

    info('*** Adding controller\n')
    net.addController('c0')

    info('*** Adding hosts\n')
    h1 = net.addHost('h1', ip='10.0.0.1')
    h2 = net.addHost('h2', ip='10.0.0.2')

    info('*** Adding switches\n')
    s1 = net.addSwitch('s1')

    info('*** Creating links\n')
    net.addLink(h1, s1)
    net.addLink(h2, s1)

    info('*** Starting network\n')
    net.start()

    # Introduce delay on switch s1's s1-eth2 interface
    h1.cmdPrint('sudo tc qdisc add dev h1-eth0 root handle 1: netem delay 20ms')
    h1.cmdPrint('sudo tc qdisc add dev s1-eth2 parent 1: handle 2: tbf rate 10gbit burst 5000000 limit 15000000')
    time.sleep(5)  # Wait 5 seconds

    # Test connectivity with ping
    info('*** Testing connectivity with ping\n')
    h1.cmdPrint('ping -c 4 10.0.0.2')

    h2.cmdPrint('iperf3 -s &')

    h1.cmdPrint('iperf3 -c 10.0.0.2')

    # Set TCP buffer size
    info('*** Setting TCP buffer size\n')
    h1.cmdPrint('sysctl -w net.ipv4.tcp_rmem="10240 87380 52428800"')
    h1.cmdPrint('sysctl -w net.ipv4.tcp_wmem="10240 87380 52428800"')
    h2.cmdPrint('sysctl -w net.ipv4.tcp_rmem="10240 87380 52428800"')
    h2.cmdPrint('sysctl -w net.ipv4.tcp_wmem="10240 87380 52428800"')

    # Start iPerf3 server on h2
    info('*** Starting iPerf3 server on h2\n')
    h2.cmdPrint('iperf3 -s &')

    # Run iPerf3 client on h1
    info('*** Running iPerf3 client on h1\n')
    h1.cmdPrint('iperf3 -c 10.0.0.2 -J >  res_lab8_1.txt')

    # Stop network
    info('*** Stopping network\n')
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    BDPExperiment()
