all: ping.png throughput.pdf

ping.png:
	sudo python lab10_1.py

throughput.pdf:
	xdg-open throughput.pdf > /dev/null 2>&1
	sudo pkill iperf3
