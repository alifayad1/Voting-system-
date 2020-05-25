#Ali Fayad (ahf27) - Anis Amer (ana53)
#This is the Voting Server.

from socket import *
from time import time
from phe import paillier
import pickle

def calculateFinal(allVotes):
    finalResult = [0, 0, 0, 0, 0]
    for i in range(5):
        sum=0
        for j in range(5):
            sum+=int(allVotes[j][i])
        finalResult[i] = sum
    
    fr = ""
    for i in range(5):
        fr = fr + str(finalResult[i])
    return fr

def new_calculate_final(allVotes):
    
    sum = 0
    for i in range(len(allVotes)):
        sum += allVotes[i]
    return sum
##############################################################################################################
print('Voting started; can receive encrypted votes from clients.')
serverPort = 8889
serverSocket = socket(AF_INET, SOCK_DGRAM)

# port 8889
serverSocket.bind(('', serverPort))

# voting ends when everyone votes or if a specifc time passes (1 hour in this case)
countVotes = 0
timeElapsed = 0

# this list contains all the votes as binary strings.
allVotes = []

startingTime = time()
while((countVotes < 3) and (timeElapsed < (3600*1000))):    # 3600000 ms is 1 hour
    message, address = serverSocket.recvfrom(1048576)  
    # received vote, parse it and count it.
    if(message != ''):
        print('Received a vote from a client.')
        countVotes += 1
        allVotes.append(pickle.loads(message))

    timeElapsed = time() - startingTime

###########################################################################################################

print("Voting is now finished; calculating the final result and sending it to the trustee server.")

trusteeName = '127.0.0.1'
trusteePort = 8888

finalResult = new_calculate_final(allVotes)

serverSocket.sendto(pickle.dumps(finalResult), (trusteeName, trusteePort))

print("Voting server done")