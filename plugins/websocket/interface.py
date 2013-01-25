# Copyright (c) 2013 LE GOFF Vincent
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


"""Module containing the websocket plugin Interface."""

from abc import *

from ext.aboard.plugin.plugin import Plugin

class Interface(Plugin, metaclass=ABCMeta):
    
    """Interface representing the WebSocket plugins.
    
    This class should define the abstract methods needed by the
    plugin.  Python will refuse to instanciate the plugin if some
    of this abstract methods are not defined in the subclass.  This
    is a guarantee for the user who could use this class as a base
    for the plugin documentation.
    
    The websocket plugin is designed to:
        Add the websocket server to the simple webserver
        Manage connections and disconnections on websocket points
        Send and receive datas with the connected clients.
    
    The main useful class for the user defined by this module is
    the WebSocketHandler class.  It is used to define a websocket
    entry point, that is an address where a client could connect to,
    but also some basic functions the client could perform on this URL.
    
    For instance, if you want to develop a Instant Messaging chat
    using websockets, you have to create, in your bundle, a class that
    will inherit from WebSocketHandler and will define some functions
    (like connect, disconnect, change_pseudo, send_message, kick_user...)
    that a connected client could perform.  The link between the
    client's side (written in JavaScript with jQury) and the server's
    side (written in your handler) is done through JSON requests.
    
    This mechanism is more detailed in the handler file of this
    plugin.
    
    """
    
    pass
