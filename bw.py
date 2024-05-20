import iperf3
import click
import csv
from datetime import datetime


FILENAME = "data.csv"

@click.group()
def grp():
	pass


@click.command()
@click.option('--port', '-p', default=5201, help="PORT")
def server(port):
	server = iperf3.Server()
	server.port = port
	tries = 1
	while True:
		server.run()
		print(f"Test completed {tries}")
		tries+=1

@click.command()
@click.option('--streams', '-P', default=1, help="STREAMS")
@click.option('--time', '-t', default=10, help="TIME DURATION")
@click.option('--interval', '-i', default=2, help="INTERVAL")
@click.option('--port', '-p', default=5201, help="PORT")
@click.option('--reverse', '-R', default=False, help="REVERSE, BIDIRECTIONAL TESTING")
@click.argument('ipadd')
def client(streams, time, interval, port, reverse, ipadd):
	nowtime = datetime.now()
	client = iperf3.Client()
	client.server_hostname = ipadd
	client.num_streams = streams
	client.duration = time
	client.jitter_ms = interval
	client.port = port
	if reverse == True:
		client.reverse == True
	result = client.run()
	

	header = ["TIMESTAMP", "THROUGHPUT_UPLINK(AVG)", "THROUGHPUT_DOWNLINK(AVG)"]
	data = [nowtime, result.sent_Mbps//streams, result.received_Mbps//streams]
	with open(FILENAME, "a", newline="") as file:
		writer = csv.writer(file)
		if file.tell() == 0:
			writer.writerow(header)
		writer.writerow(data)

grp.add_command(server)
grp.add_command(client)



if __name__ == '__main__':
	grp()

