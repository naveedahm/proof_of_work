# echo-client.py

import socket
import hashlib
import constants
import time

HOST = constants.SERVER_IP  # The server's hostname or IP address
PORT =  constants.SERVER_PORT  # The port used by the server
last_block_hash = ""
version = 1.0

def getValidNonceString(str_auth_client):
    global last_block_hash
    nonce = 1

    while True:

        # Header is being constructed
        nonceString = str(nonce) + str_auth_client + last_block_hash + str(time.time()) + str(version)

        # Computing hash of the header
        hash_string = hashlib.sha256(nonceString.encode('utf-8')).hexdigest()
        last_block_hash = hash_string

        zeroes_string = "".ljust(constants.CHALLENGE_LENGTH, "0")

        if(hash_string[0:constants.CHALLENGE_LENGTH] == zeroes_string):
            print("challenge solved ... nonce found with specified beginning zeros")
            break
        else:
            nonce = nonce + 1

    return nonceString

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b"RequestToPrintQuote")
    data = s.recv(1024)
    print(f"Received {data!r}")
    str_auth_client = data.decode()

    if(str_auth_client == constants.CHALLENGE_STRING):
        # Generate a nonce so the hash would begin with two 00s
        # TODO : the number of 0s to be generated in beginning should also be returned from the server 
        valid_nonce_string = getValidNonceString(str_auth_client)
        s.sendall(bytes(valid_nonce_string, 'utf-8'))
        data = s.recv(1024)
        print("Quote received from server is" + data.decode())
    elif(str_auth_client == constants.INVALID_CHALLENGE_MESSAGE):
        print("Challenge was not accepted by server.")

