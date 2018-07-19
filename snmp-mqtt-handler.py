#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2010-2013 Roger Light <roger@atchoo.org>
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Eclipse Distribution License v1.0
# which accompanies this distribution.
#
# The Eclipse Distribution License is available at
#   http://www.eclipse.org/org/documents/edl-v10.php.
#
# Contributors:
#    Roger Light - initial implementation
# Copyright (c) 2010,2011 Roger Light <roger@atchoo.org>
# All rights reserved.

# This shows a simple example of waiting for a message to be published.

#import context  # Ensures paho is in PYTHONPATH
import paho.mqtt.client as mqtt
from pysnmp.entity.rfc3413.oneliner import cmdgen
import time


printed = "Wasnt' printed"
old_value = 20000
def on_connect(mqttc, obj, flags, rc):
    print("rc: " + str(rc))


def on_message(mqttc, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))


def on_publish(mqttc, obj, mid):
    print("mid: " + str(mid))
    pass


def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_log(mqttc, obj, level, string):
    print(string)


mqttc = mqtt.Client()
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe


mqttc.connect("5.45.114.8", 1883, 60)

mqttc.loop_start()


while(1):
   
   print(printed)
   time.sleep(1)
   errorIndication, errorStatus, errorIndex, varBindTable = cmdgen.CommandGenerator().bulkCmd(
               cmdgen.CommunityData('test-agent', 'public'),
               cmdgen.UdpTransportTarget(('192.168.40.38', 161)),
               0,
               1,
               (1,3,6,1,4,1,1347,42,2,1,1,1,6,1)
           )

   if errorIndication:
      print(errorIndication)
   else:
       if errorStatus:
           print ('%s at %s\n' % (
               errorStatus.prettyPrint(),
               errorIndex and varBindTable[-1][int(errorIndex)-1] or '?'
               ))
       else:
          

          for varBindTableRow in varBindTable:
             for name, val in varBindTableRow:
                if name.prettyPrint() == 'SNMPv2-SMI::enterprises.1347.42.2.1.1.1.6.1.1':
                   
                   print ( '%s = %s' % (name.prettyPrint(), val))

                   
                   value = int(val.prettyPrint())
                   if value >= old_value+1:
                      print("Printing....")
                      printed = "Printed"
                      infot = mqttc.publish("/System1/toner_supply1", "", qos=2)

                      infot.wait_for_publish()
                   else:
                      printed = "Was't Printed"
                   old_value = value
                   print(old_value)
   
   
            
