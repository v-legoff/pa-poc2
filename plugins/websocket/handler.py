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


"""Module containing the abstract class WebSocketHandler."""

import json

import cherrypy
from ws4py.websocket import WebSocket
from ws4py.messaging import TextMessage

class WebSocketHandler(WebSocket):
    
    """Abstract class containing a websocket handler.
    
    A handler is a websocket entry point.  It defines a special route
    on the server where a Websocket server could be reached (for
    instance, http://myhostname.ext/ws).  It also provides a way to
    define functions that could be called by the client.  Usually,
    the client should take care of the displaying process whereas the
    server should take care of everything else (identification,
    authentication, validation...).
    
    If you want to create a Instant Messaging chat system using
    websocket, for instance, the client should only:
        Display the messages it receives from the server
        Send the server some messages back when needed.
    
    The client should send JSON messages to the server containing:
        type -- the functions's name that should be called
        data -- the data types.
    
    Here is an example of message that a client could send:
        {
            "type": "say",
            "datas": {
                "message": "Do you hear me?"
            }
        }
    
    If the message is properly decoded, the server will call a
    function with the named parameters 'message="Do your hear me?"'.
        
    To set a method as "a function that the client could call", you
    must register it in the 'functions' class attribute.  This is
    a dictionary, containing the functions's name as key and the
    expected informations as value.
    
    Here's en example:
        class Chat(WebSocketHandler):
            
            functions = {
                "say": {"message": str},
            }
            
            # ...
            def handle_say(self, message):
                "Function called when the 'say' message is sent."
    
    When the JSON message (see above) is sent, the function is called:
        handler.handle_say("Do you hear me?")
    
    In the 'functions' dictionary, the value should be a dictionary
    containing, as keys, the expected informations (message in the
    example) and as values the corresponding type of expected
    data.  If the server requested a str but the client sends an
    int, the request will be dropped.
    
    Class attributes:
        handlers -- the list of handlers (one handler byu connected client)
        ws_point -- the name of the URL where the handler should listen
    
    Methods defined in this class:
        send_JSON -- send a JSON message to the connected handler
        opened -- the handler (client) is now connected
        closed -- the connected handler (client) has disconnected
    
    """
        
    handlers = []
    ws_point = ""
    functions = ()
    
    def opened(self):
        """Method called when the handler's connection has succeeded.
        
        This method adds the newly connected handler to the list of
        handlers (WebSocketHandler.handlers).  It can be redefined in
        a subclass to perform other operations, but remember to call
        the parent method in the redefinition.
        
        """
        self.handlers.append(self)
    
    def closed(self, code, reason="A client left the room without a proper explanation."):
        """The connection had been closed.
        
        This method removes the connected handlers from the list of connected handlers (WebSocketHandler.handlers).  You can redefine it in a subclass, but remember to call the parent method in the redefinition.
        
        """
        if self in self.handlers:
            self.handlers.remove(self)
    
    def received_message(self, message):
        """Receive a message.
        
        This method expects a message in the JSON format.  It is
        responsible for reading the message, decoding, finding the
        proper function called by the message, check that the expected
        datas are of the good type and call the function with the
        specified arguments.
        
        """
        try:
            msg = message.data.decode("utf-8")
        except UnicodeError:
            return
        
        # The data should be in JSON format
        try:
            data = json.loads(msg)
        except ValueError:
            return
        
        if not isinstance(data, dict):
            return
        
        if "data" not in data or "type" not in data:
            return
        
        key = data["type"]
        args = data["data"]
        if not isinstance(key, str) or not isinstance(args, dict):
            return
        
        # Now we know what name is the function to call
        # We try to find it in the functions
        if key not in self.functions:
            return
        
        schema = self.functions[key]
        
        # Now we validate the schema
        valid = self.validate_schema(schema, args)
        if not valid:
            return
        
        function_name = "handle_" + key
        function = getattr(self, function_name)
        function(**args)
    
    @classmethod
    def validate_schema(cls, schema, args):
        """Return whether the specified schema is valid or not.
        
        A schema is a collection.  The schema and the argument
        should be of the same type.
        
        For instance, here are some datas:
            {
                "name": "vincent",
                "height": 5
            }
        
        And here is a corresponding schema:
            {
                "name": str,
                "height": int
            }
        
        """
        if not isinstance(schema, type(args)):
            return False
        
        if isinstance(schema, dict):
            keys = tuple(schema.keys())
        elif isinstance(schema, list):
            keys = tuple(range(len(schema)))
        
        for key in keys:
            try:
                value = args[key]
            except (IndexError, KeyError):
                return False
            
            sc_type = schema[key]
            if isinstance(sc_type, (dict, list)):
                ret = cls.validate_schema(sc_type, value)
                if not ret:
                    return False
            elif not isinstance(value, sc_type):
                return False
        
        return True
    
    def send_text(self, text):
        """Send a message to the websocket.
        
        This method is a wrapper for the 'send' method.
        It shouldn't be calle directly, though.  Prefer the
        'send_JSON' method.
        
        """
        msg = TextMessage(text)
        self.send(msg)
    
    def send_JSON(self, function_name, **kwargs):
        """Send the JSON corresponding to the function call."""
        datas = {
            "type": function_name,
            "data": kwargs,
        }
        text = json.dumps(datas)
        self.send_text(text)
