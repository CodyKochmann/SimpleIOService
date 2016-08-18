# -*- coding: utf-8 -*-
# @Author: codykochmann
# @Date:   2016-08-18 09:33:17
# @Last Modified 2016-08-18
# @Last Modified time: 2016-08-18 09:39:51

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
import thread

class SimpleIOService(object):
    """ This is an easy to use class that acts as a wrapper for
        any function. The benefit of using something like this
        is that it will provide you a lightweight layer that will
        give you all of the functionality to create an IO service
        in pure Python without needing to load a bulky server
        library that was designed to do that and a whole lot more.
    """
    def __init__(self, service_function):
        self.service_function = service_function


def threaded_function_service(conn,input_function):
    """ takes data in a port and responds with a function output """
    collected=''
    while 1:
        data = conn.recv(256)
        print 'parsing: {}'.format(data)
        if data.startswith('submit'):
            break
        if data.endswith("\n") and len(data) is 2:
            data = data[:-2]
            break
        if not data:
            break
        collected+=data
    try:
        reply=input_function(collected)
    except Exception, e:
        reply=e
        pass
    print "responding with: {}".format(reply)
    conn.send(reply)
    conn.close()

def SimpleIOService(input_function, host='', port=8080):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # set up the socket's settings
    try:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen(5)
    except socket.error as e:
        print(str(e))
    # run an infinite loop that will host this service
    while True:
        conn, addr = s.accept()
        print('connected to: '+addr[0]+':'+str(addr[1]))
        thread.start_new_thread(threaded_function_service,(conn,input_function))

# test code below
if __name__ == "__main__":
    def test_function(input_string):
        """ returns the length of the string given to the function """
        return "recieved string with the length of: {}".format(len(input_string))

    SimpleIOService(test_function, port=5559)


