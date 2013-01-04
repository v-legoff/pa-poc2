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


"""Module containing the PluginManager class."""

class PluginManager:
    
    """Class containing the plugin's manager.
    
    This object should contains the plugins defined by the user.  A
    plugin is a set of code containing some functionality which will
    extend the Python Aboard abilities.  For more informations about
    plugins, see the Plugin class (defined in the plugin module of
    the same package).
    
    """
    
    def __init__(self):
        self.plugins = {}
        self.subscribers = {
            "extend_configuration": [],
        }
    
    def __getattr__(self, name):
        """Return the plugin, if found."""
        return self.plugins[name]
    
    def register(self, name, plugin):
        """Register a new plugin in the manager.
        
        The plugin should be a class inherited from Plugin.
        
        """
        self.plugins[name] = plugin
        plugin.manager = self
        plugin.subscribe()
    
    def subscribe(self, plugin, event):
        """Subscribe a plugin to a particular event.
        
        This method should not be used directly by a plugin.  The event
        parameter should be the event's name.
        
        """
        subscribed = self.subscribers[event]
        subscribed.append(plugin)
        
    def call(self, event, *args, **kwargs):
        """Call the subscribed plugins."""
        subscribed = self.subscribers[event]
        for plugin in subscribed:
            method = getattr(plugin, event)
            method(*args, **kwargs)
