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


"""This module contains the different pattern types."""

types = {}

class PatternMetaclass(type):
    
    """Metaclass to insert the inherited class in the TYPES dictionary."""
    
    def __init__(cls, name, parents, attributes):
        type.__init__(cls, name, parents, attributes)
        if cls.name:
            types[cls.name] = cls

class PatternType(metaclass=PatternMetaclass):
    
    """Abstract class which represents a pattern type.
    
    The 'pattern' used in this context is a part of a route.  This pattern
    isused to represent dynamic part in a route.  For instance, in the route
    'images/:id', the ':id' part is dynamic and the 'id' part is the
    'pattern type id'.
    
    In a route description, the patterns are specified after a colons (':').
    
    To add a new pattern type, simply inherit from this class and specify
    the value of the 'name' class attribute.  For instance:
    >>> class ID(PatternType):
    ...     name = "id"
    That's it:  if the Python file containing this code is imported (of
    course), the pattern will be automaticcaly added to the usable pattern
    types.  You should be able to use it in a route description.
    
    A pattern type needs some informations:
    
    Class attributes:
        regex -- the regular expression as a str [1]
    
    Instance methods:
        convert -- convert the dynamic part (still str)
    
    """
    
    name = None #  Specify it in a subclass
    regex = None #  Specify it in a subclass
    
    def convert(self, expression):
        """Return the converted expression if possible.
        
        If not, raise a PatternError exception.
        
        """
        raise NotImplementedError


class ID(PatternType):
    
    """Patter type: id.
    
    This pattern type expects an ID, an integer > 0.
    
    """
    
    name = "id"
    regex = r"\d+"
    
    def convert(self, expression):
        """Return the converted expression if possible.
        
        If not, raise a PatternError exception.
        
        """
        # We know that the regex has been matched, so you can relax
        expression = int(expression)
        return expression
