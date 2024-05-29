import iperf3
import click
import csv
from datetime import datetime
import os
import time as tm


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



def procces_data(duration):
	with click.progressbar(length=duration, label='Processing') as bar:
		for _ in range(duration):
			time.sleep(1)
			bar.update(1)




def cl(streams, time, interval, port, reverse, ipadd, counter, protocol):
	arr=[]

	for i in range(0, time, interval):
		nowtime = datetime.now()
		formatted_time = nowtime.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
		client = iperf3.Client()
		client.server_hostname = ipadd
		client.num_streams = streams
		client.duration = interval
		client.jitter_ms = interval
		client.port = port
		client.protocol = protocol
		if protocol == 'tcp':
			prot = 'T'
		else:
			prot = 'U'	
		if reverse == True:
			client.reverse == True
		result = client.run()
		test_id = counter
		#print(f"[{test_id}]", nowtime, result.sent_Mbps, result.received_Mbps)
		#return [test_id, nowtime, result.sent_Mbps, result.received_Mbps]
		arr.append([test_id, prot, formatted_time, f"{result.sent_Mbps:.3f}", f"{result.received_Mbps:.3f}"])
		client = None

	return arr









@click.command()
@click.option('--port', '-p', default=5201, help="PORT")
def client(port):
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
@click.option('--protocol', '-h', default='tcp', help="PROTOCOL")
@click.argument('ipadd')
def server(streams, time, interval, port, reverse, protocol, ipadd):
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
	print("Start testing")
	filename, counter = get_filename()
	data = cl(streams, time, interval, port, reverse, ipadd,counter, protocol)
	
	header = ["ID", "T/U", "TIMESTAMP", "UPLINK", "DOWNLINK"]
	with open(filename, "a", newline="") as file:
		writer = csv.writer(file)
		if file.tell() == 0:
			writer.writerow(header)
		for i in data:
			writer.writerow(i)
	print("End testing")



grp.add_command(server)
grp.add_command(client)



if __name__ == '__main__':
	grp()

