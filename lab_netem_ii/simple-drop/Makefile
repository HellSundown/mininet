all: ping.dat ping.png

ping.dat:
	sudo python lab_netem_ii.py
	sudo chown mininet:mininet ping.dat

ping.png: ping.dat
	./ping_plot

clean:
	-rm -f *.dat *.png

