all: throughput.json throughput.png

throughput.json:
	sudo python lab9_1.py
	sudo chown mininet:mininet throughput.json

throughput.png: throughput.json
	sudo ./throughput_plot

clean:
	rm -f *.json *.png
