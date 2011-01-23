import hashlib
import socket
import struct
#from Peer import *

INFINITY = float('inf')

# MSGS
MSG_ACCEPT = 1
MSG_REJECT = 2
MSG_PREPARE = 3
MSG_PROPOSE = 4
MSG_PERFORM = 5
MSG_REMOVE = 6
MSG_PING = 7
MSG_ERROR = 8
MSG_HELO = 9
MSG_HELOREPLY = 10
MSG_NEW = 11

# STATES
LEADER_ST_INITIAL = 20
LEADER_ST_PREPARESENT = 21
LEADER_ST_PROPOSESENT = 22
LEADER_ST_ACCEPTED = 23
LEADER_ST_REJECTED = 24

# SCOUT RETURN VALUES
SCOUT_ADOPTED = 30
SCOUT_BUSY = 31
SCOUT_PREEMPTED = 32

# COMMANDER RETURN VALUES
COMMANDER_CHOSEN = 40
COMMANDER_BUSY = 41
COMMANDER_PREEMPTED = 42

# Lengths
MAXPROPOSALLENGTH = 20
PVALUELENGTH = 32
PEERLENGTH = 24
ADDRLENGTH = 15

# This function hashes any given string
def hash(name):
    return hashlib.md5(name).hexdigest()

def findOwnIP():
#    return socket.gethostbyname(socket.gethostname())
    return socket.gethostbyname(socket.gethostname())

# This function computes a NodeID given an addr and port
def computeNodeID(addr, port):
    name = addr+str(port)
    return hash(name)

def from_str_to_dict(self, string):
    string = string.rstrip("-")
    items = [s for s in string.split("-") if s]
    dictionary = {}
    for item in items:
        key,value = item.split("/")
        dictionary[key] = value
    return dictionary
    
def from_dict_to_str(self, dictionary):
    string = ""
    for key in dictionary:
        string += key + "/" + str(dictionary[key]) + "-"
    return string

def from_neighbors_to_str(self, neighbor_list):
    liststr = ''
    for peer in neighbor_list:
        peerstr = "%s:%d:%s" % (peer.addr, peer.port, peer.ID)
        liststr = liststr + "/" + peerstr
    return liststr

def from_str_to_neighbors(self, string):
    neighbors = []
    string = string.rstrip("/")
    peers = string.split("/")
    for peer in peers:
        peercontents = peer.split(":")
        #p = Peer(peercontents[0], peercontents[1])
        #neighbors.append(p)
    return neighbors

# pvalue calculations
# Returns the union of two pvalue arrays
def union(pvalues1, pvalues2):
    for pvalue in pvalues2:
        if pvalue in pvalues1:
            pass
        else:
            pvalues1.append(pvalue)

# Returns the max of a pvalue array            
def max(pvalues):
    maxpvalue = pvalue(ballotnumber=(0,0),commandnumber=0,proposal="")
    for pvalue in pvalues:
        if pvalue > maxpvalue:
            maxpvalue = pvalue
    return maxpvalue

class scoutReply():
    def __init__(self, giventype=0, givenballotnumber=0, givenpvalues=[]):
        self.type = giventype
        self.ballotnumber = givenballotnumber
        self.pvalues = givenpvalues
#        self.lock = Lock()
        
    def __str__(self):
        returnstr = "Scout Reply\nType: %d\nBallotnumber: %d\n" % (self.type, self.ballotnumber)
        if len(self.pvalues) > 0:
            returnstr += "Pvalues:\n"
            for pvalue in self.pvalues:
                returnstr += str(pvalue)
        return returnstr        
        
class commanderReply():
    def __init__(self, giventype=0, givenballotnumber=0, givencommandnumber=0):
        self.type = giventype
        self.ballotnumber = givenballotnumber
        self.commandnumber = givencommandnumber
#        self.lock = Lock()

    def __str__(self):
        return "Commander Reply\nType: %d\nBallotnumber: %d\nCommandnumber: %d" % (self.type, self.ballotnumber, self.commandnumber)