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


"""This module contains the StaticRoute class."""

import re

import cherrypy

from ext.aboard.router.route import Route

class StaticRoute:
    
    """A static route definition for the Python Aboard dispatcher.
    
    Static routes serve static content (CSS file, JavaScript scripts, ect).
    
    """
    
    format_dependent = True
    def __init__(self, pattern, root_dir):
        """Create a new route.
        
        Expected parameters:
            pattern -- the pattern representing the match
            root_dir -- the absolute path of the root directory
        
        """
        Route.__init__(self, pattern, None, cherrypy.lib.static.serve_file)
        self.root_dir = root_dir
    
    def __repr__(self):
        return "<StaticRoute to {} -> {})>".format(
                self.pattern, self.root_dir)
    
    def match(self, request, path):
        """Return whether or not thie path is matched by the route."""
        match = self.re_pattern.search(path)
        if match:
            static = match.groups()[0]
            static = self.root_dir + "/" + static
            return (static, )
        
        return False
    
    def convert_pattern_to_re(self, pattern):
        """Return the regular expression corresponding to the specified pattern.
        
        If errors are found, this method will raise specific
        exceptions inherited from PatternError.
        
        """
        re_pattern = "^" + pattern + "/(.+)$"
        py_pattern = pattern + "/{}"
        self.py_pattern = py_pattern
        return re.compile(re_pattern)
