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


"""Module containing the AutoLoader class."""

from imp import reload
import inspect
import importlib

from ext.aboard.autoloader.rules import DEFAULT

class AutoLoader:
    
    """Class containing the autoloader's behaviour.
    
    The AutoLoader objects are meant to import Pythohn files and extract
    their content.  Plus, they will keep in memory the loaded modules
    and will be able to automatically reload them (to upgrade some
    code without restarting the server).
    
    It's also possible to define multiple importation rules:  this
    is quite useful when something need to be done before or after
    a file is read.  For isntance, each time a file containing a
    model is realoded, it should set the data connector, otherwise
    it won't be able to read and write datas from the data storage.
    
    """
    
    def __init__(self, server):
        self.server = server
        self.loaded_modules = {}
        self.rules = {}
    
    def add_rule(self, name, rule):
        """Add a new rule.
        
        Expected arguments:
            name -- the name of the rule, shouldn't be used
            rule -- the Rule object containing the rule behavior
        
        A rule is a object whose class has inherited from Rule (see the
        rule package).
        
        """
        if name in self.rules:
            raise ValueError("this rule name is already used")
        
        self.rules[name] = rule
    
    def add_default_rule(self, name, rule):
        """Add a default rule.
        
        This method is automatically called by 'add_default_rules.  It
        is used to get the needed parameters to build the rule and call
        the 'add_rule' method with the newly created rule.
        
        """
        # Get the needed parameters
        parameters = dict(inspect.signature(rule).parameters)
        for p_name in list(parameters.keys()):
            if p_name not in self.parameters:
                raise ValueError("the {} parameter can not be found in " \
                        "the autoloader".format(repr(p_name)))
            
            parameters[p_name] = self.parameters[p_name]
        
        # We build the rule with the parameters
        rule = rule(**parameters)
        self.add_rule(name, rule)
    
    def add_default_rules(self):
        """Add the default rules defined in the DEFAULT dictionary.
        
        This method should be called by the server before any autoload.
        It adds the default rules automatically.
        
        """
        self.parameters = {
            'data_connector': self.server.data_connector,
        }
        
        for name, rule in DEFAULT.items():
            self.add_default_rule(name, rule)
    
    def load_module(self, rule, path):
        """Load a specific module dynamically.
        
        Expected arguments:
            rule -- the rule's name
            path -- the Python path to the module (package.subpackage.module)
        
        The rule determine how the specified module be imported but mostly
        what information should be loaded from it.  Most modules
        are loaded and a class contained in it is returned.
        
        """
        if rule not in self.rules:
            raise ValueError("the rule {} is not defined.".format(rule))
        
        rule_name = rule
        rule = self.rules[rule_name]
        module = importlib.import_module(path)
        ret = rule.load(module)
        self.loaded_modules[path] = module
        return ret
    
    def reload_module(self, path):
        """Reload the module to integrate changes.
        
        The module should have been previously imported by the
        autoloader.
        
        """
        # Here, it depends of Cherrypy, not implemented yet
        pass
