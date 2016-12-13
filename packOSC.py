from pythonosc import osc_message_builder
from pythonosc import udp_client
import socket
import time
import numpy as np

# #######################################################################

host = 'localhost'
port = 8888
oscClient = udp_client.UDPClient(host, port)

########################################################################

def bank(group, index):
    oscMsg = osc_message_builder.OscMessageBuilder(address="/Bank")
    oscMsg.add_arg(group)
    oscMsg.add_arg(index)
    oscMsg = oscMsg.build()
    oscClient.send(oscMsg)

def valueA(value):
    oscMsg = osc_message_builder.OscMessageBuilder(address="/Value_A")
    oscMsg.add_arg(value)
    oscMsg = oscMsg.build()
    oscClient.send(oscMsg)


def valueB1(value):
    oscMsg = osc_message_builder.OscMessageBuilder(address="/Value_B1")
    oscMsg.add_arg(value)
    oscMsg = oscMsg.build()
    oscClient.send(oscMsg)

def valueB2(value):
    oscMsg = osc_message_builder.OscMessageBuilder(address="/Value_B2")
    oscMsg.add_arg(value)
    oscMsg = oscMsg.build()
    oscClient.send(oscMsg)

def valueB3(value):
    oscMsg = osc_message_builder.OscMessageBuilder(address="/Value_B3")
    oscMsg.add_arg(value)
    oscMsg = oscMsg.build()
    oscClient.send(oscMsg)

def valueB4(value):
    oscMsg = osc_message_builder.OscMessageBuilder(address="/Value_B4")
    oscMsg.add_arg(value)
    oscMsg = oscMsg.build()
    oscClient.send(oscMsg)

def release():
    oscMsg = osc_message_builder.OscMessageBuilder(address="/Release")
    oscMsg = oscMsg.build()
    oscClient.send(oscMsg)

########################################################################
