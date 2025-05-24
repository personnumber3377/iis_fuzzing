
import socket
import os
import struct
import copy
import pickle
import string

from http_mutator import * # Get all the shit...

CHUNK_SIZE = 4096*10
TIMEOUT_MS = 50
RECV_AMOUNT = 100
MAX_CORP_SIZE = 30_000 # 30k samples maximum

def load_corpus(directory): # Loads the corpus shit from the thing...
    corp = []

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

            corp.append(copy.deepcopy(chunk))


    return corp

HOW_MANY_TO_KEEP = 10000
# SAVE_COUNT = 200_000 # 200k should suffice right?
SAVE_COUNT = 1000*100 # Save every 100k requests...

def save_corpus(corpus):
    random_string = ''.join(random.choices(string.ascii_letters, k=10))
    fn = random_string+".pkl"
    with open(fn, "wb") as f:
        pickle.dump(corpus, f)
    print("[+] Saved corpus to "+str(fn)+" !!!")
    return

def send_files(directory, host, port):
    # with socket.create_connection((host, port)) as sock:

    corpus = load_corpus(directory)

    previous_requests = [None] * HOW_MANY_TO_KEEP
    tot_count = 0
    while True: # Main fuzz loop
        # print("Doing the stuff....")

        # i = 0
        for testcase in corpus:
            # print("i == "+str(i))
            # i += 1
            tot_count += 1
            if tot_count % SAVE_COUNT == 0:
                save_corpus(corpus)
            # Now mutate 
            # old_chunk = copy.deepcopy(chunk)
            chunk = mutate_http(testcase)
            #if chunk != old_chunk:
            #    print("poopoo!!!")


            try:
                sock = socket.create_connection((host, port))
                sock.settimeout(TIMEOUT_MS / 1000.0)
                sock.sendall(chunk)
                stuff = sock.recv(RECV_AMOUNT)
                if b"400" not in stuff:
                    # print(stuff)
                    corpus.append(chunk) # Add the new shit in the thing...

                    if len(corpus) >= MAX_CORP_SIZE:
                        corpus.pop(random.randrange(0, len(corpus) - 1)) # Just delete a random element from the thing....
                sock.close()
            except TimeoutError:
                continue
            except OSError:
                with open("previous_requests.pkl", "wb") as f:
                    pickle.dump(previous_requests, f)
                fh = open("exploit.bin", "wb")
                fh.write(chunk)
                fh.close()
                print("Crashed the thing!!!!")
                exit(0)
            # Keep the fifo running...
            previous_requests.append(chunk)
            previous_requests.pop(0)
            assert len(previous_requests) == HOW_MANY_TO_KEEP # Should stay the same...
            assert len(corpus) <= MAX_CORP_SIZE # Should always be at most this here...

            # Send zero-length filename to indicate end
            # sock.sendall(struct.pack('!I', 0))




if __name__ == "__main__":
    # 192.168.50.29
    # send_files("./payloads/", "192.168.50.29", 80)

    # send_files("./payloads/", "192.168.50.29", 80)

    send_files("./good_corp/", "192.168.50.29", 80)
