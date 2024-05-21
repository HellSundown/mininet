#!/usr/bin/env python
""" Router's Buffer Size experiment. Output: ping.dat """
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
    net.addLink(h1, s1)
    net.addLink(h2, s2)
    net.addLink(h3, s1)
    net.addLink(h4, s2)
    net.addLink(s1, s2)
    info('*** Starting network\n')
    net.start()

    # Modify hosts' buffer size
    for host in [h1, h3, h2, h4]:
        host.cmd('sysctl -w net.ipv4.tcp_rmem=\'10240 87380 131072000\'')
        host.cmd('sysctl -w net.ipv4.tcp_wmem=\'10240 87380 131072000\'')

    s1.cmdPrint('sudo tc qdisc add dev s1-eth1 root handle 1: netem delay 10ms')
    s2.cmdPrint('sudo tc qdisc add dev s2-eth1 root handle 1: netem delay 10ms')

    s1.cmdPrint('sudo tc qdisc add dev s1-eth1 parent 1: handle 2: tbf rate 10gbit burst 5000000 limit 160000')
    h2.cmdPrint('iperf3 -s &')
    h4.cmdPrint('iperf3 -s &')
    h1.cmdPrint('iperf3 -c 10.0.0.2 -t 90 > res_1_ping-h1.txt')
    h3.cmdPrint('iperf3 -c 10.0.0.2 -t 90 > res_2_ping-h3.txt')

    h1.cmdPrint('sysctl -w net.ipv4.tcp_congestion_control=reno')
    h2.cmdPrint('iperf3 -s &')
    h4.cmdPrint('iperf3 -s &')
    h1.cmdPrint('iperf3 -c 10.0.0.2 -t 90 > res_3_ping-h1.txt')
    h3.cmdPrint('iperf3 -c 10.0.0.2 -t 90 > res_4_ping-h3.txt')

    h1.cmdPrint('sysctl -w net.ipv4.tcp_congestion_control=bbr')
    h2.cmdPrint('iperf3 -s &')
    h4.cmdPrint('iperf3 -s &')
    h1.cmdPrint('iperf3 -c 10.0.0.2 -t 90 > res_5_ping-h1.txt')
    h3.cmdPrint('iperf3 -c 10.0.0.2 -t 90 > res_6_ping-h3.txt')

    s1.cmdPrint('sudo tc qdisc add dev s1-eth1 parent 1: handle 2: tbf rate 10gbit burst 5000000 limit 26214400')

    h1.cmdPrint('sysctl -w net.ipv4.tcp_congestion_control=cubic')
    h2.cmdPrint('iperf3 -s &')
    h4.cmdPrint('iperf3 -s &')
    h1.cmdPrint('iperf3 -c 10.0.0.2 -t 90 > res_7_ping-h3.txt')
    h3.cmdPrint('iperf3 -c 10.0.0.2 -t 90 > res_8_ping-h3.txt')

    h1.cmdPrint('sysctl -w net.ipv4.tcp_congestion_control=reno')
    h2.cmdPrint('iperf3 -s &')
    h4.cmdPrint('iperf3 -s &')
    h1.cmdPrint('iperf3 -c 10.0.0.2 -t 90 > res_9_ping-h3.txt')
    h3.cmdPrint('iperf3 -c 10.0.0.2 -t 90 > res_10_ping-h3.txt')

    h1.cmdPrint('sysctl -w net.ipv4.tcp_congestion_control=bbr')
    h2.cmdPrint('iperf3 -s &')
    h4.cmdPrint('iperf3 -s &')
    h1.cmdPrint('iperf3 -c 10.0.0.2 -t 90 > res_11_ping-h3.txt')
    h3.cmdPrint('iperf3 -c 10.0.0.2 -t 90 > res_12_ping-h3.txt')

    s1.cmdPrint('sudo tc qdisc change dev s1-eth1 root handle 1: netem delay 10ms loss 0.01%')

    h1.cmdPrint('sysctl -w net.ipv4.tcp_congestion_control=cubic')
    h2.cmdPrint('iperf3 -s &')
    h4.cmdPrint('iperf3 -s &')
    h1.cmdPrint('iperf3 -c 10.0.0.2 -t 90 > res_13_ping-h3.txt')
    h3.cmdPrint('iperf3 -c 10.0.0.2 -t 90 > res_14_ping-h3.txt')

    h1.cmdPrint('sysctl -w net.ipv4.tcp_congestion_control=reno')
    h2.cmdPrint('iperf3 -s &')
    h4.cmdPrint('iperf3 -s &')
    h1.cmdPrint('iperf3 -c 10.0.0.2 -t 90 > res_15_ping-h3.txt')
    h3.cmdPrint('iperf3 -c 10.0.0.2 -t 90 > res_16_ping-h3.txt')

    h1.cmdPrint('sysctl -w net.ipv4.tcp_congestion_control=bbr')
    h2.cmdPrint('iperf3 -s &')
    h4.cmdPrint('iperf3 -s &')
    h1.cmdPrint('iperf3 -c 10.0.0.2 -t 90 > res_17_ping-h3.txt')
    h3.cmdPrint('iperf3 -c 10.0.0.2 -t 90 > res_18_ping-h3.txt')

    info('*** Stopping network\n')
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    emptyNet()

