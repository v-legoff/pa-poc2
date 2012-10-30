# Copyright (c) 2012 LE GOFF Vincent
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# * Neither the name of the copyright holder nor the names of its contributors
#   may be used to endorse or promote products derived from this software
#   without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
# OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


"""Module containing the WebsocketServer class.

This class is used to create a Websocket server, listening on a specified
port (most of the time on localhost anyway).  This server should be
launched when the web server itself is launched.  This class does
not modify the behavior of the web server in itself and; web server
and the websocket server will be accessed through different ports.

"""

import select
import socket
import threading
from socket import AF_INET, SOCK_STREAM

class WebsocketServer(threading.Thread):
    
    """TCP server specially designed for web sockets.
    
    This websocket server is executed in a main thread.  Typically,
    a new connection will be handled as follow:
    1.  The server accepts it and waits for its first request
    2.  The first client message should be a upgrade request (handshake 1)
    2.  The server answers with another request (handshake 2)
    3.  The connection is then placed in the 'connected' list
    4.  The client and the server can send datas to each other
    X.  Until the connection ends.
    
    Expected parameters:
        host -- the host on which to listen for connections
        port -- the port on which to listen for connections
    
    """
    
    def __init__(self, host="0.0.0.0", port=9621):
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self.server_socket = socket.socket(AF_INET, SOCK_STREAM)
        self.clients = []
        self.connections = []
    
    def run(self):
        """Run the thread, launch the server."""
        # Bind and make listen the server socket
        print("Bind the websocket server.")
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.server_socket.accept()
        print("Accepted, terminate")
