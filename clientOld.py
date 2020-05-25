#Ali Fayad (ahf27) - Anis Amer (ana53)
# This is the code on the client side.

import sys
from socket import *

def valid(vote):
    return True

def encodeVote(vote):      # vote = "1-2-3"
    result = [0, 0, 0, 0, 0]

    votearr = vote.split("-")
    for i in range(len(votearr)):
        result[int(votearr[i])-1] = 1
        
    res = ""
    for i in range(len(result)):
        res+=str(result[i])
    return res
##########################################################################################################
print("client server started")
trusteeName = '127.0.0.1'
trusteePort = 8888

# TCP connection
# transfer data to both Trustee and Voting Servers.
clientSocket = socket(AF_INET, SOCK_DGRAM)

print("Here's the list of names you can vote for:")
print("1. Donald Trump\n2. Roger Federer\n3. Britney Spears")
print("4. Dalai Lama\n5. Steve Jobs")
print("Choose the numbers you want separated by '-'.")
print("Examples on valid voting: 1-2-3; 2-3-4-5 ; 1-2")
vote = input("Examples on invalid votes: 1,2-4 ; 6 ; trump-2\n")

clientSocket.sendto(encodeVote(vote).encode(), (trusteeName, trusteePort))

received = False

while(not received):
    encryptedVote, address = clientSocket.recvfrom(1048576)
    if(encryptedVote != ''):
        received = True
print("encrypted vote received ")
#############################3#############################################################################

votingName = '127.0.0.1'
votingPort = 8889

clientSocket.sendto(encryptedVote, (votingName, votingPort))

# assume that the voting was successfull
print("You voted successfully.")
sys.exit()

