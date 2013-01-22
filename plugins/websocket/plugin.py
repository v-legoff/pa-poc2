import cherrypy

from ws4py.server.cherrypyserver import WebSocketPlugin, WebSocketTool

from ext.aboard.plugin import Plugin as AbsPlugin
from plugins.websocket.handler import WebSocketHandler

class Plugin(AbsPlugin):
    
    """Class containing the websocket plugin.
    
    This plugin is designed to handle the websockets.  It uses
    the ws4py library (and the Cherrypy plugin that it provides)
    to handle the websockets.
    
    """
    
    subscribe_to = ("extend_server_configuration", )
    
    @classmethod
    def extend_server_configuration(cls, engine, config):
        """Extend the server configuration."""
        cp_plugin = WebSocketPlugin(engine)
        cp_plugin.subscribe()
        cls.cp_plugin = cp_plugin
        cherrypy.tools.websocket = WebSocketTool()
        WebSocketHandler.handlers = cp_plugin.pool
        config.update({
            '/ws': {
                'tools.websocket.on': True,
                'tools.websocket.handler_cls': WebSocketHandler,
            },
        })
