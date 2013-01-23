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
    
    handlers = []
    functions = ()
    
    def opened(self):
        """The connection has succeeded."""
        self.handlers.append(self)
    
    def closed(self, code, reason="A client left the room without a proper explanation."):
        """The connection had been closed by the client."""
        print("quit", code, reason)
        if self in self.handlers:
            self.handlers.remove(self)
    
    def received_message(self, m):
        msg = m.data.decode("utf-8")
        
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
        
        # Now we know what name is the function to dcall
        # We try to find it in the handlers
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
        print("send", key, args)
    
    @staticmethod
    def validate_schema(schema, args):
        return True
    
    def send_text(self, text):
        """Send a message to the websocket.
        
        This method is a wrapper for the 'send' method.
        
        """
        print("Send out", text)
        msg = TextMessage(text)
        self.send(msg)
    
    def send_JSON(self, function_name, **kwargs):
        """Send the JSON corresopnding to the function call."""
        datas = {
            "type": function_name,
            "data": kwargs,
        }
        text = json.dumps(datas)
        self.send_text(text)
