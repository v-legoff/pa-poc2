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


import os

import yaml

"""Module containing the Config class, descripbed below."""

class Config:
    
    """Class representing the bundle configurations.
    
    Precise files in the bundle configuration directory (bundle_name/config)
    are read and analyzed at setup.
    
    """
    
    def __init__(self, bundle_name):
        """Construct the configuration."""
        self.configurations = {}
        path = "bundles/" + bundle_name + "/config"
        if os.path.exists(path):
            for file_name in os.listdir(path):
                if file_name.endswith(".yml") and len(file_name) > 4:
                    file_path = path + "/" + file_name
                    with open(file_path, "r") as file:
                        print("Reading configuration file", file_path)
                        configuration = yaml.load(file)
                        self.configurations[file_name[:-4]] = configuration
    
    def setup(self, server):
        """Setup the configuration."""
        self.setup_routes(server)
        return True
    
    def setup_routes(self, server):
        """Setup the routes found in 'routing' configuration file."""
        if "routing" not in self.configurations:
            return
        
        for name, informations in self.configurations["routing"].items():
            pattern = informations.get("pattern", "")
            if not pattern.startswith("/"):
                pattern = "/" + pattern
            
            # Try to find the controller
            location = informations["controller"]
            print(location)
            bundle_name, controller_name, action_name = location.split(".")
            bundle = server.bundles[bundle_name]
            controller = bundle.controllers[controller_name]
            action = getattr(controller, action_name)
            methods = informations.get("method")
            
            params = []
            if methods:
                params = [methods]
            
            server.dispatcher.add_route(pattern, controller, action, *params)
