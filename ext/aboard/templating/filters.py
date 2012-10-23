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


"""Module containing the TemplateFilters class."""

class TemplateFilters:
    
    """Class containing the templates filters.
    
    The methods defined in this class are usable as filters
    inside Jinja2 templates.  New methods are atuomatically added to
    the list of filters.
    
    For instance, if you define an instance method like that:
    >>>     def wiki(self, text):
    You can call it in a template like that:
        "some text"|wiki
    
    The first argument ('self' as in any instance methods) is used
    to reach global informations, such as the server.
    
    """
    
    def __init__(self, server, filters):
        """Initialize and add the functions."""
        for name in dir(self):
            function = getattr(self, name)
            if not callable(function):
                continue
            
            if name.startswith("_"):
                continue
            
            print("filter", name)
            filters[name] = function
        
        self.server = server
    
    def wiki(self, text):
        """Return the wiki formatted text."""
        wiki_service = self.server.services.wiki
        return wiki_service.convert_text(text)
