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
    h5 = net.addHost('h5', ip='10.0.0.5')
    h6 = net.addHost('h6', ip='10.0.0.6')
    h7 = net.addHost('h7', ip='10.0.0.7')
    h8 = net.addHost('h8', ip='10.0.0.8')
    info('*** Adding switches\n')
    s1 = net.addSwitch('s1')
    s2 = net.addSwitch('s2')
    info('*** Creating links\n')
    net.addLink(h1, s1)
    net.addLink(h2, s2)
    net.addLink(h3, s1)
    net.addLink(h4, s2)
    net.addLink(h5, s1)
    net.addLink(h6, s2)
    net.addLink(h7, s1)
    net.addLink(h8, s2)
    net.addLink(s1, s2)
    info('*** Starting network\n')
    net.start()

    s1.cmdPrint('sudo tc qdisc add dev s1-eth1 root handle 1: netem delay 20ms')
    s1.cmdPrint('sudo tc qdisc add dev s1-eth1 parent 1: handle 2: tbf rate 10gbit burst 5000000 limit 15000000')

    h1.cmdPrint("sysctl -w net.ipv4.tcp_rmem='10240 87380 52428800'")
    h1.cmdPrint("sysctl -w net.ipv4.tcp_wmem='10240 87380 52428800'")
    h2.cmdPrint("sysctl -w net.ipv4.tcp_rmem='10240 87380 52428800'")
    h2.cmdPrint("sysctl -w net.ipv4.tcp_wmem='10240 87380 52428800'")

    h2.cmdPrint('iperf3 -s &')
    h1.cmdPrint('iperf3 -c 10.0.0.2')

    info('*** Stopping network\n')
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    emptyNet()
