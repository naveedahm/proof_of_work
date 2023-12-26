# echo-client.py

import socket
import hashlib
import constants

HOST = constants.SERVER_IP  # The server's hostname or IP address
PORT =  constants.SERVER_PORT  # The port used by the server

def getValidNonceString(str_auth_client):
    nonce = 1
    while True:
        nonceString = str(nonce) + str_auth_client
        final_nonce_string = hashlib.sha256(nonceString.encode('utf-8')).hexdigest()

        # TODO Make this code dynamic for dynamic number of 0s to be used in front of it
        challenge_string = "".ljust(constants.CHALLENGE_LENGTH, "0")

        if(final_nonce_string[0:constants.CHALLENGE_LENGTH] == challenge_string):
            print("challenge solved ... nonce found with specified beginning zeros")
            break
        else:
            nonce = nonce + 1
        #print(final_nonce_string)
        #print(nonce)
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
    else if(str_auth_client == constants.INVALID_CHALLENGE_MESSAGE):
        print("Challenge was not accepted by server.")

        


        


