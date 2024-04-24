import iperf3

port = int(input("Enter port: "))

server = iperf3.Server()
server.port = port
n=1
while True:
<<<<<<< HEAD
	server.run()
	print(f'Test completed {n}')
	n+=1
print('Test errored')
=======
  server.run()
  print(f"Test completed {n}")
  n+=1
print("Test errored")
>>>>>>> 98316c2216239503c2f1272410a129f8201013b0
