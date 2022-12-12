#   In order to write this parser at home, I needed bytes objects (in the 
# formatting as seen in lab). The easiest way I found to do this was to save 
# the bytes object as a string (using bytes.hex() function) to a text file. 
# There are 100% better ways to do this, but this was for testing only and is 
# not meant for production use.
#
# The sdnParser and printPKTinfo libraries will be used just as 
# they would be in lab, taking in bytes objects
#
# please see each imported library for more information
#
# This is used for testing only
#
from PPP.functions import print_Packet
from PPP.functions import Packet_Parser
from PPP.functions import make_library
import os
# make_library.make_library()




packets = open('PPP/library/test_cases.txt','r').readlines()


# for each line in the text file, 
# ex hex_string = 'ff59a300c763a8f2' (type: string)
for hex_string in packets[:]:
    os.system('cls')

    # convert the line into it's intended bytes object
    pkt = bytes.fromhex(hex_string)

    # create an object with the packet's information parsed
    Packet = Packet_Parser.Parser(pkt)

    # print the objects information to console
    print_Packet.Printer(Packet)

    # to make sure I am deleting large description dictionaries
    # print(psutil.Process().memory_info().rss / (1024*1024))





