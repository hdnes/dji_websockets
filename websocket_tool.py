#!/usr/bin/python

import binascii
import uuid

from websocket import *
ws = create_connection("ws://localhost:19870/general")

#{"SEQ":"12345","CMD":""} - Get command list on any service. 
#{"SEQ":"12345","CMD":"get_info"} - Serial Number & User Token
#{"SEQ":"12345","CMD":"read","INDEX":"fly_limit_height"} - Read fly_limit_height
#{"SEQ":"12345","CMD":"write","INDEX":"fly_limit_height", "VALUE":111} - Set fly_limit_height ( limited by Max value )

ws.settimeout(2)
try:
    appstatus =  ws.recv()
    appversion =  ws.recv()
    appflags =  ws.recv()
    configstatus =  ws.recv()
    devicestatus =  ws.recv()
    pcstatus =  ws.recv()

    deviceHash = devicestatus.split(",")[3].strip().split(":")[1].split('"')[1] # Extract Hash_ServiceID
    print "Connecting to " + deviceHash
    print "------------------"
    devConfigURL = "ws://localhost:19870/controller/config/user/" + deviceHash
    ws.close

    if devicestatus.find(devConfigURL):
        print "Connecting to " + devConfigURL
        ws = create_connection(devConfigURL)
        commands = ws.recv()
        # print commands

#        if commands.find("read"):
#            print "Reading g_config_flying_limit_height_limit_enabled over the websocket"
#            ws.send('{"SEQ":"' + str(uuid.uuid4().get_hex().upper()[0:6]) + '","CMD":"read","INDEX":"g_config_flying_limit_height_limit_enabled"}')
#            result = ws.recv()
#            print result
#        else:
#            print "No read command available in the Websocket API for this service"

        result = ws.recv()
        print result

        if commands.find("write"):
            #-------- disable altitude restriction --------
            print "Disabling Altitude Restrictions"
            ws.send('{"SEQ":"' + str(uuid.uuid4().get_hex().upper()[0:6]) + '","CMD":"write","INDEX":"g_config_flying_limit_height_limit_enabled", "VALUE":1}')
            result = ws.recv()
            print result
            result = ws.recv()
            print result
            #-------- raise altitude restriction --------
            print "Disabling Altitude Restrictions"
            ws.send('{"SEQ":"' + str(uuid.uuid4().get_hex().upper()[0:6]) + '","CMD":"write","INDEX":"fly_limit_height", "VALUE":1000}')
            result = ws.recv()
            print result
            result = ws.recv()
            print result
            #------------ disable No Fly Zones ------------
            print "Disabling No Fly Zones"
            ws.send('{"SEQ":"' + str(uuid.uuid4().get_hex().upper()[0:6]) + '","CMD":"write","INDEX":"g_config_airport_limit_cfg_cfg_limit_data", "VALUE":20250910}')
            result = ws.recv()
            print result
            result = ws.recv()
            print result

        else:
            print "No write command available in the Websocket API for this service"
    else:
        print "Necessary Service is not present"


except WebSocketTimeoutException as e:
    print e

ws.close()
