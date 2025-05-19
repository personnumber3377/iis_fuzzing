
import socket
import os
import struct
import copy

from generic_mutator_bytes import * # Get all the shit...

CHUNK_SIZE = 4096*10
TIMEOUT_MS = 50
RECV_AMOUNT = 100

def send_files(directory, host, port):
    # with socket.create_connection((host, port)) as sock:

    while True: # Main fuzz loop

        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            # print("Running: "+str(filepath))
            if os.path.isfile(filepath):
                # Send filename length and filename
                # encoded_name = filename.encode()
                # sock.sendall(struct.pack('!I', len(encoded_name)))
                # sock.sendall(encoded_name)

                # Send file size and content
                # filesize = os.path.getsize(filepath)
                # sock.sendall(struct.pack('!Q', filesize))
                # mutate_generic

                # mutate_generic


                f = open(filepath, 'rb')

                ''' as f:
                    while chunk := f.read(CHUNK_SIZE):
                        sock.sendall(chunk)
                '''

                chunk = f.read() # Read file

                f.close()

                # Now mutate 
                old_chunk = copy.deepcopy(chunk)
                chunk = mutate_generic(chunk)
                #if chunk != old_chunk:
                #    print("poopoo!!!")


                try:
                    sock = socket.create_connection((host, port))
                    sock.settimeout(TIMEOUT_MS / 1000.0)
                    sock.sendall(chunk)
                    stuff = sock.recv(RECV_AMOUNT)
                    # if b"400" not in stuff:
                    #     print(stuff)

                    sock.close()
                except TimeoutError:
                    continue
                except OSError:
                    fh = open("exploit.bin", "wb")
                    fh.write(chunk)
                    fh.close()


            # Send zero-length filename to indicate end
            # sock.sendall(struct.pack('!I', 0))

if __name__ == "__main__":
    # 192.168.50.29
    # send_files("./payloads/", "192.168.50.29", 80)

    send_files("./payloads/", "192.168.50.29", 80)

