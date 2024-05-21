#!/usr/bin/env python

"""
Lab 7: Understanding Rate-based TCP Congestion Control (BBR)
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

    info( '*** Creating links\n' )
    net.addLink( h1, s1 )
    net.addLink( s1, s2 )
    net.addLink( s2, h2 )

    info('*** Starting network\n')
    net.start()

    time.sleep(2)  # Wait for network convergence

    # Emulate packet loss on switch S1's s1-eth2 interface
    info('*** Introducing packet loss rate on switch S1\n')
    s1.cmdPrint('sudo tc qdisc add dev s1-eth2 root handle 1: netem loss 0.01%')

    # Modify bandwidth of link between switches
    info('*** Modify bandwidth of link between switches\n')
    s1.cmdPrint('sudo tc qdisc add dev s1-eth2 parent 1: handle 2: tbf rate 1gbit burst 500000 limit 2500000')

    # Change TCP congestion control algorithm to Reno on h1
    info('*** Changing TCP congestion control algorithm to Reno on h1\n')
    h1.cmdPrint('sysctl -w net.ipv4.tcp_congestion_control=reno')

    # Launch iPerf3 server on h2
    info('*** Launching iPerf3 server on h2\n')
    h2.cmdPrint('iperf3 -s &')

    # Launch iPerf3 client on h1 with TCP Reno
    info('*** Launching iPerf3 client on h1 with TCP Reno\n')
    h1.cmdPrint('iperf3 -c 10.0.0.2 -t 20 -O 10 -J > reno_results.json')

    # Change TCP congestion control algorithm to BBR on h1
    info('*** Changing TCP congestion control algorithm to BBR on h1\n')
    h1.cmdPrint('sysctl -w net.ipv4.tcp_congestion_control=bbr')

    # Launch iPerf3 server on h2
    info('*** Launching iPerf3 server on h2\n')
    h2.cmdPrint('iperf3 -s &')

    # Launch iPerf3 client on h1 with TCP BBR
    info('*** Launching iPerf3 client on h1 with TCP BBR\n')
    h1.cmdPrint('iperf3 -c 10.0.0.2 -t 20 -O 10 -J > bbr_results.json')

    # Add delay to switch S1's s1-eth2 interface
    info('*** Adding delay to switch S1\n')
    s1.cmdPrint('sudo tc qdisc change dev s1-eth2 root handle 1: netem loss 0.01% delay 30ms')

    # Modify TCP buffer size on h1
    info('*** Modifying TCP buffer size on h1\n')
    h1.cmdPrint('sysctl -w net.ipv4.tcp_rmem=\'10240 87380 150000000\'')
    h1.cmdPrint('sysctl -w net.ipv4.tcp_wmem=\'10240 87380 150000000\'')

    # Modify TCP buffer size on h2
    info('*** Modifying TCP buffer size on h2\n')
    h2.cmdPrint('sysctl -w net.ipv4.tcp_rmem=\'10240 87380 150000000\'')
    h2.cmdPrint('sysctl -w net.ipv4.tcp_wmem=\'10240 87380 150000000\'')

    # Change TCP congestion control algorithm to Reno on h1
    info('*** Changing TCP congestion control algorithm to Reno on h1\n')
    h1.cmdPrint('sysctl -w net.ipv4.tcp_congestion_control=reno')

    # Launch iPerf3 server on h2
    info('*** Launching iPerf3 server on h2\n')
    h2.cmdPrint('iperf3 -s &')

    # Create and enter reno directory on h1
    info('*** Creating and entering reno directory on h1\n')
    h1.cmdPrint('mkdir reno && cd reno')

    # Launch iPerf3 client on h1 with TCP Reno and save results to reno.json
    info('*** Launching iPerf3 client on h1 with TCP Reno and saving results\n')
    h1.cmdPrint('iperf3 -c 10.0.0.2 -t 30 -J > reno.json')
    h1.cmdPrint('plot_iperf.sh reno.json')

    # Navigate to results directory
    info('*** Navigating to results directory\n')
    h1.cmdPrint('cd results/')

    # Open generated files
    info('*** Opening generated files\n')
    h1.cmdPrint('zathura throughput.pdf')
    h1.cmdPrint('zathura cwnd.pdf')
    h1.cmdPrint('cd ../')

    # Change TCP congestion control algorithm to BBR on h1
    info('*** Changing TCP congestion control algorithm to BBR on h1\n')
    h1.cmdPrint('sysctl -w net.ipv4.tcp_congestion_control=bbr')

    # Launch iPerf3 server on h2
    info('*** Launching iPerf3 server on h2\n')
    h2.cmdPrint('iperf3 -s &')

    h1.cmdPrint('mkdir bbr && cd bbr')
    h1.cmdPrint('iperf3 -c 10.0.0.2 -t 30 -J > bbr.json')
    h1.cmdPrint('plot_iperf.sh bbr.json')
    h1.cmdPrint('cd results/')

    # Open generated files
    info('*** Opening generated files\n')
    h1.cmdPrint('zathura throughput.pdf')
    h1.cmdPrint('zathura cwnd.pdf')
    h1.cmdPrint('cd ../')

    info('*** Stopping network\n')
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    emptyNet()
