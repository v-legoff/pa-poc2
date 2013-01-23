import json

import cherrypy
from ws4py.websocket import WebSocket
from ws4py.messaging import TextMessage

class WebSocketHandler(WebSocket):
    handlers = {
        "message": {},
    }
    pool = {}
    
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
        if key not in self.handlers:
            return
        
        schema = self.handlers[key]
        
        # Now we validate the schema
        valid = self.validate_schema(schema, args)
        if not valid:
            return
        
        function_name = "handle_" + key
        function = getattr(self, function_name)
        function(**args)
        print("send", key, args)
    
    def closed(self, code, reason="A client left the room without a proper explanation."):
        print("quit", code, reason)
        cherrypy.engine.publish('websocket-broadcast', TextMessage(reason))
    
    @staticmethod
    def validate_schema(schema, args):
        return True
    
    def handle_message(self, message):
        print("I recieved", message)
        encap = {'type': 'message', 'data': {'message': message}}
        encap = json.dumps(encap)
        cherrypy.engine.publish('websocket-broadcast', TextMessage(encap))
