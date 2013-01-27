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

import hashlib
import os

import cherrypy
from cherrypy._cptools import HandlerTool
import yaml

from ext.aboard.autoloader import AutoLoader
from ext.aboard.bundle import Bundle
from ext.aboard.controller import Controller
from ext.aboard.dc import connectors
from ext.aboard.formatters import formats
from ext.aboard.formatters.base import Formatter
from ext.aboard.model import Model
from ext.aboard.plugin.manager import PluginManager
from ext.aboard.router.dispatcher import AboardDispatcher
from ext.aboard.server.plugins.reloader import Reloader
from ext.aboard.service import Service
from ext.aboard.service.manager import ServiceManager
from ext.aboard.templating import Jinja2

class Server:
    
    """Wrapper of a cherrypy server."""
    
    def __init__(self):
        self.host = "127.0.0.1"
        self.port = 9000
        self.hostname = "localhost"
        self.dispatcher = AboardDispatcher()
        self.loader = AutoLoader(self)
        self.bundles = {}
        self.configurations = {}
        self.plugin_manager = PluginManager(self)
        self.services = ServiceManager()
        self.services.register_defaults()
        self.templating_system = Jinja2(self)
        self.templating_system.setup()
        
        Controller.server = self
        Formatter.server = self
        Service.server = self
    
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
        # Update the server's host and port
        if "server" in self.configurations:
            server = self.configurations["server"]
            if "host" in server:
                self.host = server["host"]
            if "port" in server:
                self.port = server["port"]
            if "hostname" in server:
                self.hostname = server["hostname"]
        
        # DataConnector configuration
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
        dc.running = True
        Model.data_connector = dc
        
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
        
        self.data_connector = dc
        self.default_format = default
        self.allowed_formats = allowed_formats
        self.loader.add_default_rules()
    
    def load_bundles(self):
        """Load the user's bundles."""
        path = "bundles"
        for name in os.listdir(path):
            if not name.startswith("__") and os.path.isdir(path + "/" + name):
                bundle = Bundle(self, name)
                self.bundles[name] = bundle
        
        for bundle in self.bundles.values():
            bundle.setup(self, self.loader)
    
    def run(self):
        """Run the server."""
        cherrypy.engine.autoreload.unsubscribe()
        cherrypy.engine.reloader = Reloader(cherrypy.engine)
        cherrypy.engine.reloader.loader = self.loader
        cherrypy.engine.reloader.subscribe()
        abs_path = os.path.abspath(os.path.join(os.path.dirname(
                __file__), "..", "..", ".."))
        print("abspath", abs_path)
        cherrypy.config.update({
                'server.socket_host': self.host,
                'server.socket_port': self.port,
                'tools.staticdir.root': abs_path,
        })
        cherrypy.config["tools.encode.on"] = True
        cherrypy.config["tools.decode.on"] = True
        config = {
            '/static': {
                'tools.staticdir.on': True,
                'tools.staticdir.dir': 'static',
                'tools.staticdir.content_types': {
                        'ogg': 'application/ogg',
                }
            }
        }
        
        # Some plugins add configuration
        self.plugin_manager.call("extend_server_configuration", cherrypy.engine, config)
        print("config", config)
        cherrypy.tree.mount(root=self.dispatcher, config=config)
        cherrypy.engine.start()
        cherrypy.engine.block()
    
    def get_model(self, name):
        """Try and retrieve a Model class."""
        bundle_name, model_name = name.split(".")
        bundle = self.bundles[bundle_name]
        model = bundle.models[model_name]
        return model
    
    def get_cookie(self, name, value=None):
        """Get the cookie and return its value or 'value' if not found."""
        try:
            return cherrypy.request.cookie[name].value
        except KeyError:
            return value
    
    def set_cookie(self, name, value, max_age, path="/", version=1):
        """Set a cookie."""
        cookie = cherrypy.response.cookie
        cookie[name] = value
        cookie[name]['path'] = path
        cookie[name]['max-age'] = max_age
        cookie[name]['version'] = 1
    
    def authenticated(self):
        """Return whether the current request is authenticated or not."""
        client_token = self.get_cookie("PA-client-token")
        if not client_token:
            print("no cookie")
            return False
        
        headers = cherrypy.request.headers
        if "Remote-Addr" not in headers:
            print("no IP")
            return False
        
        to_hash = "Python-Aboard " + headers.get("Remote-Addr", "none")
        to_hash += " " + headers.get("User-Agent", "unknown")
        to_hash = to_hash.encode()
        token = hashlib.sha256(to_hash).digest()
        return client == client_token
