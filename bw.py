import iperf3
import click
import csv


FILENAME = "datas.csv"

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
@click.argument('ipadd')
def client(streams, time, interval, port, ipadd):
	client = iperf3.Client()
	client.server_hostname = ipadd
	client.num_streams = streams
	client.duration = time
	client.jitter_ms = interval
	client.port = port
	result = client.run()
	

	data = [result.time, result.sent_bytes, result.received_bytes, result.sent_bps]

	with open(FILENAME, "a", newline="") as file:
		head = ["TIME", " SENT BYTES", " RECEIVED BYTES", " SENT BPS"]
		writer = csv.writer(file)
		writer.writerow(head)
		writer.writerow(data)	


grp.add_command(server)
grp.add_command(client)



if __name__ == '__main__':
	grp()

