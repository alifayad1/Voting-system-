#Ali Fayad (ahf27) - Anis Amer (ana53)
# This is the trustee server

from phe import paillier
import pickle

public_key, private_key = paillier.generate_paillier_keypair()
# votes [1, 2, 3, 4, 5] for example.
def decodeVote(votes):
    votes = str(votes)
    candidates={
       0:'Donald Trump',
       1:'Roger Federer',
       2:'Britney Spears',
       3:'Dalai lama',
       4:'Steve Jobs' 
    }
    maximum = 0
    for i in range(1,5):
        if(votes[i] > votes[maximum]):
            maximum = i
	winner = candidates[maximum]
    return winner
#########################################################################################################
from socket import *
from time import time

print('trustee server started; we can receive from other servers.')

trusteePort = 8888
trusteeSocket = socket(AF_INET, SOCK_DGRAM)
trusteeSocket.bind(('', trusteePort))
#################################################################################################

receivedFromClients = 0
timeElapsed = 0

print("Waiting for elections to finish.")
startingTime = time()
while((receivedFromClients < 3) and (timeElapsed < (3600*1000))):
    vote, clientAddress = trusteeSocket.recvfrom(1048576)
    if(vote != ''):

        receivedFromClients+=1
        encryptedVote = public_key.encrypt(int(vote));
        trusteeSocket.sendto(pickle.dumps(encryptedVote), clientAddress)

    timeElapsed = time() - startingTime

###################################################################################################

print("Finished voting")
# voting has finished, receive the final result from the voting server and decrypt it.

receivedFinal = False

while(not receivedFinal):
    votes, votingAddress = trusteeSocket.recvfrom(1048576)

    if(votes != ''):
        receivedFinal = True
        result = decodeVote(private_key.decrypt(pickle.loads(votes)))
        print('The winner is: ' + result)