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


"""Module containg the Python Aboard server, build on CherryPy."""

import os

import cherrypy
import yaml

from ext.aboard.bundle import Bundle
from ext.aboard.dc import connectors
from ext.aboard.formatters import formats
from ext.aboard.formatters.base import Formatter
from ext.aboard.model import Model
from ext.aboard.router.dispatcher import AboardDispatcher
from ext.aboard.templating import Jinja2

class Server:
    
    """Wrapper of a cherrypy server."""
    
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.dispatcher = AboardDispatcher()
        self.bundles = {}
        self.configurations = {}
        self.templating_system = Jinja2(self)
        self.templating_system.setup()
        Formatter.server = self
    
    @property
    def models(self):
        """Return all the models."""
        models = []
        for bundle in self.bundles.values():
            models.extend(list(bundle.models.values()))
        
        return models
    
    
    def load_configurations(self):
        """This method reads the configuration files found in /config."""
        path = "config"
        for file_name in os.listdir(path):
            if file_name.endswith(".yml"):
                with open(path + "/" + file_name, "r") as file:
                    configuration = yaml.load(file)
                    self.configurations[file_name[:-4]] = configuration
    
    def prepare(self):
        """Prepare the server."""
        dc_conf = self.configurations["data_connector"]
        dc_name = dc_conf["dc_name"]
        dc_spec = dict(dc_conf)
        del dc_spec["dc_name"]
        try:
            dc = connectors[dc_name]
        except KeyError:
            print("Unknown data connector {}".format(dc_name))
            return
        
        dc = dc()
        dc.setup(**dc_spec)
        Model.data_connector = dc
        print("Set data connector to", dc_name)
        
        if "formats" not in self.configurations:
            return
        cfg_formats = self.configurations["formats"]
        
        # Setup the default_format
        default = cfg_formats["default_format"].lower()
        if default not in formats:
            raise ValueError("unknown format {}".format(default))
        
        allowed_formats = []
        for format in cfg_formats.get("allowed_formats", []):
            format = format.lower()
            if format not in formats:
                raise ValueError("unknown format {}".format(format))
            
            allowed_formats.append(format)
        
        self.default_format = default
        self.allowed_formats = allowed_formats
    
    def load_bundles(self):
        """Load the user's bundles."""
        path = "bundles"
        for name in os.listdir(path):
            if not name.startswith("__") and os.path.isdir(path + "/" + name):
                bundle = Bundle(name)
                self.bundles[name] = bundle
        
        for bundle in self.bundles.values():
            bundle.setup(self)
    
    def run(self):
        """Run the server."""
        cherrypy.config.update({'server.socket_port': 9000})
        conf = {'/': {'request.dispatch': self.dispatcher}}
        cherrypy.tree.mount(root=None, config=conf)
        cherrypy.engine.start()
        cherrypy.engine.block()
    
    def get_model(self, name):
        """Try and retrieve a Model class."""
        bundle_name, model_name = name.split(".")
        bundle = self.bundles[bundle_name]
        model = bundle.models[model_name]
        return model
