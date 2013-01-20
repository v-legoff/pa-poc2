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


"""Module containing the ControllerRule class."""

from ext.aboard.autoloader.rules.base import Rule

class ControllerRule(Rule):
    
    """Class defining the autoloader rule to import controllers.
    
    The controllers are module containing a class.  When a module
    containing a Controller is loaded, the class is instanciated
    and the server instance attribute is set.  The ControllerRule
    automatically register this controller (the instanciated object)
    in the bundle's controllers.
    
    """
    
    def __init__(self, server):
        self.server = server
    
    def load(self, module):
        """Load a specific module.
        
        This method:
            Get the Controller class defined in the module
            Get the controller's bundle
            Instanciate the Controller class
            Set the server instance attribute
            Write the newly created object in the bundle's controllers
            Return the object
        
        """
        bundle_name = Rule.bundle_name(module)
        bundle = self.server.bundles[bundle_name]
        name = Rule.module_name(module)
        class_name = name.capitalize()
        ctl_class = getattr(module, class_name)
        ctl_object = ctl_class(bundle)
        ctl_object.server = self.server
        
        # Write the object in the bundle
        bundle.controllers[class_name] = ctl_object
        
        # Add the controller's routes
        routes = tuple(bundle.config.routes.items())
        routes = [(name, infos) for name, infos in routes if infos[1] == \
                class_name]
        for route, (pattern, ctl_name, action, methods) in routes:
            action = getattr(ctl_object, action)
            self.server.dispatcher.add_route(route, pattern, ctl_object, \
                    action)
        
        return ctl_object
    
    def unload(self, module):
        """Unload th emodule containing the controllers.
        
        Delete all the routes connected with this controller.
        
        """
        name = Rule.module_name(module)
        class_name = name.capitalize()
        ctl_class = getattr(module, class_name)
        self.server.dispatcher.delete_routes_for_controller(ctl_class)
