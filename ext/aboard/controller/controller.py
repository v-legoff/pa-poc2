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


"""Module defining the Controller class, described below."""

from ext.aboard.formatters import formats
from ext.aboard.model.exceptions import ObjectNotFound

class Controller:
    
    """Class describing a controller, wrapper for actions.
    
    A controller is a class containing methods that will act as actions.  If a
    route is connected to an action of a controller (a method of the class),
    then it will be called when a request is sent to this route.
    
    """
    
    def __init__(self, server):
        """Build the controller."""
        self.server = server
        self.request = None
    
    @staticmethod
    def model_id(*names_of_model):
        """Decorator which takes integers and convert to object.
        
        The number of arguments should match the number of positional
        arguments expected by the callable (the method controller).
        
        If, for instance, the controler method is like that:
        >>> def view(self, user):
        then the line just above should be something like:
        >>> @Controller.model_id("User")
        
        """
        def decorator(function):
            """Main wrapper."""
            def callable_wrapper(controller, *args, **kwargs):
                """Crapper of the controller."""
                # Convert the list of arguments
                c_args = []
                for i, arg in enumerate(args):
                    model_name = names_of_model[i]
                    if model_name:
                        # Get the model
                        model = controller.server.get_model(model_name)
                        arg = int(arg)
                        try:
                            object = model.find(arg)
                        except ObjectNotFound as err:
                            return str(err)
                        
                        c_args.append(object)
                    else:
                        c_args.append(arg)
                    
                return function(controller, *c_args, **kwargs)
            return callable_wrapper
        return decorator
    
    def render(self, view, **representations):
        """Render datas using the formatters."""
        format = self.request.format
        if not format:
            format = self.server.default_format
        
        if format == "jj2":
            template = self.server.templating_system.get_template(view)
            return template.render(**representations)
        
        if format not in self.server.allowed_formats:
            return "Unknown format {}.".format(format)
        
        return formats[format].convert(**representations)
