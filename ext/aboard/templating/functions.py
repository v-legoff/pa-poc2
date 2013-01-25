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


"""Module containing the TemplateFunctions class."""

class TemplateFunctions:
    
    """Class containing the templates global functions.
    
    The methods defined in this class are usable as global functions
    inside Jinja2 templates.  New methods are atuomatically added to
    the global functions list.
    
    For instance, if you define an instance method like that:
    >>>     def link_to(self, route_name):
    You can call it in a template like that:
        link_to("route")
    
    The first argument ('self' as in any instance methods) is used
    to reach global informations, such as the server.
    
    """
    
    def __init__(self, server, globals):
        """Initialize and add the functions."""
        for name in dir(self):
            function = getattr(self, name)
            if not callable(function):
                continue
            
            if name.startswith("_"):
                continue
            
            globals[name] = function
        
        self.server = server
    
    def full_URL(self, protocol=None, host=None, port=None, path=None):
        """Return a given URL 'protocol://host:port/path'.
        
        You can specify informations through the named arguments.
            If the protocol is not specified, it will be 'http'
            If the host is not specified, it will be the server's host
            If the port is nos specified, it will be the server's port [1]
            If the path is not specified, it won't be included.
        
        [1] If the protocol is HTTP and the port 80, it is not included.
        
        """
        if protocol is None:
            protocol = "http"
        
        if host is None:
            host = self.server.hostname
        
        if port is None:
            port = self.server.port
        
        if protocol == "http" and port == 80:
            address = "{protocol}://{host}/"
        else:
            address = "{protocol}://{host}:{port}/"
        
        address = address.format(protocol=protocol, host=host, port=port)
        if path:
            address += path
        
        return address
    
    def link_to(self, route, *parameters, name="here", confirm=None):
        """Return a <a> tag.
        
        The route must be its name given in the 'routing.yml'
        configuration file.
        
        """
        try:
            route = self.server.dispatcher.routes[route]
        except KeyError:
            raise KeyError("route {} not found".format(repr(route)))
        
        if len(route.patterns) != len(parameters):
            raise ValueError("this route needs {} parameters, {} " \
                    "given".format(len(route.patterns), len(parameters)))
        
        parameters = [str(param) for param in parameters]
        href = route.get_path(*parameters) + ".jj2"
        confirmation = ""
        if confirm:
            confirmation = " onclick=\"return confirm('" + confirm + "')\""
        link = "<a href=\"{href}\"{confirmation}>{name}</a>".format(
                href=href, name=name, confirmation=confirmation)
        return link
