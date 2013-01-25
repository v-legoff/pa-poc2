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


"""Module containing the WebSocketHandlerRule class."""

from ext.aboard.autoloader.rules.base import Rule

class WebSocketHandlerRule(Rule):
    
    """Class defining the autoloader rule to import web socket handlers.
    
    A web socket handler is an object which keeps track of the
    connected clients and contain several methods called when a client
    sends a specific request.  The web socket handlers are more
    detailed in the WebSocketHandler class (contained in the 'handler'
    module of the 'websocket' package).
    
    When a WebSocketHandler is automatically loaded, the class
    containing the handler is extracted from the module, then
    returned.
    
    """
    
    def __init__(self, server):
        self.server = server
    
    def load(self, module):
        """Load a specific module.
        
        This method:
            Get the WebSocketHandler class defined in the module
            Return the class
        
        """
        name = Rule.module_name(module)
        class_name = name.capitalize()
        wsh_class = getattr(module, class_name)
        
        wsh_class.handlers = []
        if not wsh_class.ws_point:
            raise ValueError("the 'ws_point' class attribute is not " \
                    "set in {}".format(wsh_class))
        
        return wsh_class
