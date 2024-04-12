import iperf3

port = int(input("Enter port: "))

server = iperf3.Server()
server.port = port
n=1
while True:
	server.run()
	print(f'Test completed {n}')
	n+=1
print('Test errored')
