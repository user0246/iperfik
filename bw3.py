import iperf3
import click
import csv
from datetime import datetime
import os


FILENAME = "data.csv"

@click.group()
def grp():
	pass




def get_file(streams):
	nowtime = datetime.now()
	header = ["TIMESTAMP", "THROUGHPUT_UPLINK(AVG)", "THROUGHPUT_DOWNLINK(AVG)"]
	data = [nowtime, result.sent_Mbps//streams, result.received_Mbps//streams]
	with open(FILENAME, "a", newline="") as file:
		writer = csv.writer(file)
		if file.tell() == 0:
			writer.writerow(header)
		writer.writerow(data)




def get_filename():
	COUNTER_FILE = 'counter.txt'
	if not os.path.exists(COUNTER_FILE):
		counter = 0
		with open(COUNTER_FILE, 'w') as f:
			f.write(str(counter))
	else:
		with open(COUNTER_FILE, 'r') as f:
			counter = int(f.read().strip())

	counter+=1
	with open(COUNTER_FILE, 'w') as f:
		f.write(str(counter))
	
	filename = f"data_{counter}.csv"
	#print(filename, counter)
	return [filename, counter]







def cl(streams, time, interval, port, reverse, ipadd, counter):
	arr=[]
	for i in range(0, time, interval):
		nowtime = datetime.now()
		client = iperf3.Client()
		client.server_hostname = ipadd
		client.num_streams = streams
		client.duration = interval
		client.jitter_ms = interval
		client.port = port
		if reverse == True:
			client.reverse == True
		result = client.run()
		test_id = counter
		#print(f"[{test_id}]", nowtime, result.sent_Mbps, result.received_Mbps)
		#return [test_id, nowtime, result.sent_Mbps, result.received_Mbps]
		arr.append([test_id, nowtime, result.sent_Mbps, result.received_Mbps])
		client = None
	return arr










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
@click.option('--interval', '-i', default=1, help="INTERVAL")
@click.option('--port', '-p', default=5201, help="PORT")
@click.option('--reverse', '-R', default=False, help="REVERSE, BIDIRECTIONAL TESTING")
@click.argument('ipadd')
def client(streams, time, interval, port, reverse, ipadd):
#	for i in range(time):
#		nowtime = datetime.now()
#		client = iperf3.Client()
#		client.server_hostname = ipadd
#		client.num_streams = streams
#		client.duration = 1
#		client.jitter_ms = interval
#		client.port = port
#		if reverse == True:
#			client.reverse == True
#		result = client.run()
#		test_id = get_filename()[1]
#		print(test_id, nowtime, result.sent_Mbps, result.received_Mbps)
#
#		client = None
	counter = get_filename()[1]
	data = cl(streams, time, interval, port, reverse, ipadd,counter)


	filename = get_filename()[0]
	header = ["ID", "TIMESTAMP", "UPLINK", "DOWNLINK"]
	with open(filename, "a", newline="") as file:
		writer = csv.writer(file)
		if file.tell() == 0:
			writer.writerow(header)
		for i in data:
			writer.writerow(i)





grp.add_command(server)
grp.add_command(client)



if __name__ == '__main__':
	grp()

