# echo-server.py

import socket
import random
import hashlib
import constants
from threading import *

QUOTES = [
    "It always seems impossible until it's done",
    "If you're going through hell, keep going.",
    "It does not matter how slowly you go as long as you do not stop.",
    "Our greatest weakness lies in giving up. The most certain way to succeed is always to try just one more time.",
    "Good, better, best. Never let it rest. 'Til your good is better and your better is best.",
    "Failure will never overtake me if my determination to succeed is strong enough.",
    "Quality is not an act, it is a habit.",
    "Life is 10% what happens to you and 90% how you react to it."
]

def printQuote(client_connection, client_address):
    with client_connection:
        print(f"Connected by {client_address}")
        data = client_connection.recv(1024)
        # TODO : How to verify if data is received
        #if not data:
        #    break
        decoded_data = data.decode()

        if(decoded_data == constants.REQUEST_TO_PRINT_QUOTE_MESSAGE):
            print("Request to print quote received ... generating challenge")

        client_connection.sendall(constants.CHALLENGE_STRING.encode())
        data = client_connection.recv(1024)
        #if not data:
        #    break
        challenge_response = data.decode()
        print("Challenge response received from client is " + challenge_response)

        # Verify that challenge response contains the challenge sent by the server
        if(constants.CHALLENGE_STRING in challenge_response):

            encoded_challenge_response = hashlib.sha256(challenge_response.encode('utf-8')).hexdigest()

            # TODO : Make this code generic to dynamically determine the number of 0s in front of hash
            challenge_string = "".ljust(constants.CHALLENGE_LENGTH, "0")

            # Verify the challenge response
            if(encoded_challenge_response[0:constants.CHALLENGE_LENGTH] == challenge_string):
                # Valid challenge response
                print("Generating Quote ...")
                r_int = random.randint(0, len(QUOTES) - 1 )
                quote_to_print = QUOTES[r_int]
                client_connection.sendall(quote_to_print.encode('utf-8'))
            else:
                print("Challenge response is invalid")
                message = constants.INVALID_CHALLENGE_MESSAGE_0
                client_connection.sendall(message.encode('utf-8'))
        else:
                print("Challenge response is invalid")
                message = constants.INVALID_CHALLENGE_MESSAGE_1
                client_connection.sendall(message.encode('utf-8'))
        return

HOST = constants.SERVER_IP  # Standard loopback interface address (localhost)
PORT =  constants.SERVER_PORT # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

    s.bind((HOST, PORT))
    s.listen()
    while True:
        client_connection, client_address = s.accept()
        t  = Thread(target = printQuote, args=(client_connection, client_address,))
        t.start()


