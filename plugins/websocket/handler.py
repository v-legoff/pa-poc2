import cherrypy
from ws4py.websocket import WebSocket
from ws4py.messaging import TextMessage

class WebSocketHandler(WebSocket):
    handlers = {}

    def received_message(self, m):
        msg = m.data.decode("utf-8")
        self.send(TextMessage("hi"))
        cherrypy.engine.publish('websocket-broadcast', m)

    def closed(self, code, reason="A client left the room without a proper explanation."):
        print("quit", code, reason)
        cherrypy.engine.publish('websocket-broadcast', TextMessage(reason))
