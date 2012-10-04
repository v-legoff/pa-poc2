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


"""This module contains the AboardDispatcher class, defined below."""

import cherrypy
Dispatcher = cherrypy.dispatch.Dispatcher

from ext.aboard.router.route import Route

class AboardDispatcher(Dispatcher):
    
    """Cherrypy dispatcher for Python Aboard.
    
    The dispatcher contains the routing process.  The routes, defined
    in the ./route.py file, are added to this dispatcher and are used to
    redirect an HTTP request to a controller.
    
    The controllers are callables (usually instance methods) that are
    configured for a matching URI.
    
    Arguments given to this callable are:
        Positional: when the route expects resource identifiers [1]
        Keyword: the arguments given to a GET, POST or PUT method
    
    [1] Take for example the URI:
          images/1
        Here, the 'images' part won't change.  Though, the '1' part
        usually expects a integer.  This route will accept URIs like:
          images/5
          images/32
          ...
    
    """
    
    def __init__(self):
        """Construct the dispatcher for Python Aboard.
        
        Note that the translator used on the default dispatcher is
        not used here.
        
        """
        Dispatcher.__init__(self, translate={})
        self.routes = []
    
    def __call__(self, path):
        """Look for a matching route to 'path'."""
        print("call", path)
        return Dispatcher.__call__(self, path)
    
    def find_handler(self, path):
        """Return the appropriate page handler, plus any virtual path."""
        request = cherrypy.serving.request
        request.config = {"tools.encode.on": True}
        request.is_index = True
        for route in self.routes:
            print("match?", route, path, end=" ")
            if route.match(path):
                print("yes")
            else:
                print("no")
                return route.callable, route.expected_arguments
        print("not found")
        return None, []
    
    def add_route(self, pattern, controller):
        """Add a route."""
        route = Route(pattern, controller)
        self.routes.append(route)
