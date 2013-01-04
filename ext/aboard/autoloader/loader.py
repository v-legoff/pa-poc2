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
import importlib

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
    
    def __init__(self):
        self.loaded_modules = {}
        self.rules = {}
    
    def add_rule(self, name, rule):
        """Add a new rule.
        
        Expected arguments:
            name -- the name of the rule, shouldn't be used
            rule -- the class containing the rule behaviour.
        
        A rule is a class inherited from Rule (see the rule package).
        
        """
        if name in self.rules:
            raise ValueError("this rule name is already used")
        
        self.rules[name] = rule
    
    def add_default_rules(self):
        """Add the default rules."""
        for name, rule in DEFAULT.items():
            self.add_rule(name, rule)
    
    def load_module(self, rule, path, attribute):
        """Load a specific module dynamically.
        
        Expected arguments:
            rule -- the rule's name
            path -- the Python path to the module (package.subpackage.module)
            attribute -- the attribute to get from the module.
        
        If attribute is empty, then the whole module is returned.
        Otherwise, the value of the module's attribute is returned.
        
        """
        if rule not in self.rules:
            raise ValueError("the rule {} is not defined.".format(rule))
        
        rule_name = rule
        rule = self.rules[rule_name]
        module = importlib.import(path)
        rule.load(module)
        if attribute:
            ret = getattr(module, attribute)
        else:
            ret = module
        
        self.loaded_modules[path] = module
        return ret
    
    def reload_module(self, path):
        """Reload the module to integrate changes.
        
        The module should have been previously imported by the
        autoloader.
        
        """
        