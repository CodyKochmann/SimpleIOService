# -*- coding: utf-8 -*-
# @Author: cody
# @Date:   2016-08-16 09:27:53
# @Last Modified 2016-08-18
# @Last Modified time: 2016-08-18 10:50:45

"""
This is basically the interphase to the IO service. Once a machine is
running a hosted function, another machine can use this function to
run data against the function in order to spread a huge job out to
multiple machines.

One example usage of this for myself is a linear regression service.
Since linear regression is a great tool for AI to generate an
understanding of something, I would set up nodes that are ready to
crank out the linear regression of any given dataset per request. This
gave me a tool that would show things like progressing regression
patterns and allowed me to generate on the fly a universe of tests in
order to create more intelligent conclusions.
"""

import socket
from time import sleep

def send_data_to_hosted_function(data, host='', port=80):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host,port))
    s.send(data)
    sleep(0.1)
    #s.send('submit')
    response=''
    while 1:
        data = s.recv(1)
        #print "recieved: {}".format(data)
        if not data:
            break
        response += data
    s.close()
    return response


# test code below
if __name__ == '__main__':
    test_data_to_send="hello world or something like that"
    host='192.168.0.7'
    port=5566
    print send_data_to_hosted_function(test_data_to_send, host, port)
