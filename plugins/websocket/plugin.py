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


"""Module containing the websocket Plugin class."""

import cherrypy

from plugins.websocket.interface import Interface
from ws4py.server.cherrypyserver import WebSocketPlugin, WebSocketTool

from plugins.websocket.handler import WebSocketHandler
from plugins.websocket.rules.handler import WebSocketHandlerRule

class Plugin(Interface):
    
    """Class containing the websocket plugin.
    
    This plugin is designed to handle the websockets.  It uses
    the ws4py library (and the Cherrypy plugin that it provides)
    to handle the websockets.
    
    """
    
    handlers = []
    subscribe_to = (
            "bundle_autoload",
            "extend_autoloader",
            "extend_server_configuration",
    )
    
    @classmethod
    def extend_autoloader(cls, self, autoloader):
        """Add a 'ws_handler' rule to the autoloaders."""
        autoloader.add_rule("ws_handler", WebSocketHandlerRule(self))
    
    @classmethod
    def bundle_autoload(cls, bundle, autoloader):
        """Load the websocket handlers."""
        handlers = autoloader.load_modules("ws_handler",
                "bundles." + bundle.name + ".websockets")
        for handler in handlers:
            cls.handlers.append(handler)
    
    @classmethod
    def extend_server_configuration(cls, engine, config):
        """Extend the server configuration."""
        cp_plugin = WebSocketPlugin(engine)
        cp_plugin.subscribe()
        cherrypy.tools.websocket = WebSocketTool()
        for handler in cls.handlers:
            config.update({
                handler.ws_point: {
                    'tools.websocket.on': True,
                    'tools.websocket.handler_cls': handler,
                },
            })
