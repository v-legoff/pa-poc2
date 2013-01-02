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


"""This module contains the route class, a route definition."""

import re

from ext.aboard.router.patterns import types

# Constants
RE_NAME = re.compile("^([A-Za-z]+)")
ALL_METHODS = ("GET", "POST", "PUT", "DELETE")

class Route:
    
    """A route definition for the Python Aboard dispatcher.
    
    This class describes the concept of routes, which are used to
    match an URI to a corresponding callable.  When the AboardDispatcher
    receives a URI, it browses the defined routes to find one that matches
    it.  The first found one will be used and its callable will be
    called with some specific arguments.
    
    A route is identified by a pattern (converted to a regular
    expression).  Parts of the route are static while others are
    dynamic.  Consider the following example, using the regular expressions:
        images/(\d+)
    Here, the 'images/' is static.  For a user request to match
    this route, it must begin by 'images/'.  Though, after that, one
    or more numbers are expected.  Thus, the following URIs will
    match this route:
        images/1
        images/28
        images/131
    The route 'images/' WILL NOT match it, though.
    Note that, in practice, regular expressions are used behind the
    scene.  The route's patterns are easier to understand and add
    some advantages (like accept only some types of data).
    
    """
    
    format_dependent = False
    def __init__(self, pattern, controller, callable, methods=ALL_METHODS):
        """Create a new route.
        
        Expected parameters:
            pattern -- the pattern representing the match [1]
            callable -- the callable which will be called if the route matches
        
        [1] The pattern is not a regular expression but...
        
        """
        if pattern.endswith("/"):
            pattern = pattern[:-1]
        
        self.pattern = pattern
        self.controller = controller
        self.callable = callable
        if isinstance(methods, str):
            methods = [methods]
        self.methods = tuple(meth_name.upper() for meth_name in methods)
        self.patterns = []
        self.py_pattern = ""
        self.re_pattern = self.convert_pattern_to_re(pattern)
    
    def __repr__(self):
        return "<Route to {} -> {} (methods={})>".format(
                self.pattern, self.callable, ",".join(self.methods))
    
    def match(self, request, path):
        """Return whether or not thie path is matched by the route."""
        if request.method.upper() not in self.methods:
            return False
        
        match = self.re_pattern.search(path)
        if match:
            return match.groups()
        
        return False
    
    def get_path(self, *arguments):
        """Return the route with its arguments."""
        return self.py_pattern.format(*arguments)
    
    def convert_pattern_to_re(self, pattern):
        """Return the regular expression corresponding to the specified pattern.
        
        If errors are found, this method will raise specific
        exceptions inherited from PatternError.
        
        """
        re_pattern = pattern
        py_pattern = pattern
        pos = re_pattern.find(":")
        while pos >= 0:
            # Get the string from pos to the end
            sub = pattern[pos + 1:]
            # Get the string to convert
            r_name = RE_NAME.search(sub)
            if not r_name:
                raise PatternError("the pattern expression {} ends " \
                        "with a ':' whereas an expression name is " \
                        "expected".format(pattern))
            
            r_name = r_name.groups()[0]
            
            # Try to find the specified type
            type = types.get(r_name)
            if type is None:
                raise TypeExpressionNotFound("the {} expression " \
                        "was not found".format(repr(r_name)))
            
            type = type()
            re_pattern = re_pattern[:pos] + "(" + type.regex + ")" + \
                    re_pattern[pos + len(r_name) + 1:]
            py_pos = py_pattern.find(":")
            py_pattern = py_pattern[:py_pos] + "{}" + py_pattern[
                    py_pos + len(r_name) + 1:]
            pos = re_pattern.find(":")
            self.patterns.append(type)
        
        re_pattern = "^" + re_pattern + "$"
        self.py_pattern = py_pattern
        print("py", py_pattern)
        return re.compile(re_pattern)
