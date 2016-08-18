# -*- coding: utf-8 -*-
# @Author: codykochmann
# @Date:   2016-08-18 09:33:17
# @Last Modified 2016-08-18
# @Last Modified time: 2016-08-18 10:50:57

"""
This is a really lightweight socket server that
serves a python function on a network. Basically,
you have a function that provides an IO service
that is wrapped in a python function. What this
does is hosts the function on a specified port
and allows other devices to use that function to
process different things.

I specifically built this to make an IO service
for a raspberry pi network so larger ai jobs can
be broken into many little parts that each pi can
do.
"""

import socket
import threading

class SimpleIOService(object):
    """ This is an easy to use class that acts as a wrapper for
        any function. The benefit of using something like this
        is that it will provide you a lightweight layer that will
        give you all of the functionality to create an IO service
        in pure Python without needing to load a bulky server
        library that was designed to do that and a whole lot more.
    """
    def __init__(self, service_function, host='', port=8000, autostart=True):
        # set up all the variables
        self.service_function = service_function
        self.host = host
        self.port = port
        self.autostart = autostart
        # set up the socket
        try:
            self.socket = socket.socket(
                socket.AF_INET,
                socket.SOCK_STREAM
            )
            self.socket.bind((self.host,self.port))
            self.socket.listen(8) # listen to up to 8 connections at once
        except socket.error as e:
            # make this error handling use logging later
            print(str(e))
        # run the autostart if applicable
        if self.autostart:
            self.start()

    def start(self):
        print "starting new thread on {}".format(self.port)
        self.thread = threading.Thread(target=self.run, args=())
        self.thread.daemon = True  # Daemonize thread
        self.thread.start()        # Start the execution
        #self.thread = thread.start_new_thread(self.start,())

    def run(self):
        print "thread successfully starting"
        while True:
            conn, addr = self.socket.accept()
            # change this to use logging
            print('connected to: '+addr[0]+':'+str(addr[1]))
            t = threading.Thread(
                target=self.threaded_function_service,
                args=(conn,self.service_function))
            t.daemon = True
            t.start()

    def threaded_function_service(self,conn,input_function):
        """ takes data in a port and responds with a function output """
        collected=[]
        conn.settimeout(0.01)
        while 1:
            try:
                collected.append(conn.recv(1))
            except socket.timeout:
                break
        collected = ''.join(collected)
        try:
            reply=input_function(collected)
        except Exception, e:
            reply=e
            pass
        print "responding with: {}".format(reply)
        conn.send(reply)
        conn.close()


# test code below
if __name__ == "__main__":
    def test_function(input_string):
        """ returns the length of the string given to the function """
        return "recieved string with the length of: {}".format(len(input_string))

    io = SimpleIOService(test_function, port=5566)
    while True:
        raw_input('press enter to stop')

