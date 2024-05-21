#!/usr/bin/env python

"""
Enhancing TCP Throughput with Parallel Streams Experiment.
Output: throughput.json
"""

from mininet.net import Mininet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.log import setLogLevel, info
import time

def ParallelStreamsExperiment():

    "Create a network and run Parallel Streams experiment."

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

    time.sleep(10)  # Wait 10 seconds

    # Test connectivity with ping from h1 to h2
    info('*** Testing connectivity with ping\n')
    h1.cmdPrint('ping -c 4 10.0.0.2')

    # Start iPerf3 server on h2
    info('*** Starting iPerf3 server on h2\n')
    h2.cmdPrint('iperf3 -s &')

    # Run iPerf3 client with parallel streams on h1
    info('*** Running iPerf3 client with parallel streams on h1\n')
    h1.cmdPrint('iperf3 -c 10.0.0.2 -P 8 -J > throughput.json')

    # Stop network
    info('*** Stopping network\n')
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    ParallelStreamsExperiment()
