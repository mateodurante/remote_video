# Comunicate with arduino on serial port and expect web socket connections
# to send and receive comunication
# Green IT project licenced under GNU General Public Licence
# Author: Mateo Durante

import tornado
import tornado.websocket
from datetime import timedelta
import datetime, sys, time
from pprint import pprint
import json
import serial.tools.list_ports
import serial

clients = []

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    tt = datetime.datetime.now()
    def check_origin(self, origin):
        #print "origin: " + origin
        return True
    # the client connected
    def open(self):
        print ("New client connected")
        self.write_message("You are connected")
        clients.append(self)
        #tornado.ioloop.IOLoop.instance().add_timeout(timedelta(seconds=1), self.test)


    # the client sent the message
    def on_message(self, message):
        print ("message: " + message)
        try:
            #self.write_message(message)
            for c in clients:
                c.write_message(message)
        except Exception as e:
            print ("cant send value to arduino")
            #raise(e)
        #self.write_message(message)

    # client disconnected
    def on_close(self):
        print ("Client disconnected")
        clients.remove(self)

socket = tornado.web.Application([(r"/socket", WebSocketHandler),])
if __name__ == "__main__":
    socket.listen(8888)
    tornado.ioloop.IOLoop.instance().start()