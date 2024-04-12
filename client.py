import iperf3

#Enter part
ipadd = input("Enter Server IP: ")
port = int(input("Enter port: "))
streams = int(input("Enter number of streams: "))
duration = int(input("Enter test duration in seconds: "))
jitter = int(input("Enter interval in seconds: "))

client = iperf3.Client()
client.server_hostname = ipadd
client.num_streams = streams
client.duration = duration
client.jitter_ms = jitter
client.port = port
result = client.run()

if result.error:
	print(result.error)
else:
	print('Test completed')
	print(f"Time: {result.time}")
	print(f"Sent bytes: {result.sent_bytes}")
	print(f"Received bytes: {result.received_bytes}")
	print(f"Sent bps: {result.sent_bps}")
	#print(result.json)	JSON OUTPUT
