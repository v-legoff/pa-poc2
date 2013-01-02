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


"""Module containing the Servicemanager class."""

import os

from ext.aboard.service.default import defaults

class ServiceManager:
    
    """Class containing the server's services.
    
    Each service is represented by a class.  Each time
    a service is called (see __getattr__), an instance of
    this service is created and will exist as long as
    it is needed.
    
    The services are also stored in the 'services'
    dictionary ({name: class}).  Note that:
    >>> manager.service #  will create a new service instance
    Whereas:
    >>> manager["service"] #  will return the service class
    
    """
    
    def __init__(self):
        """Build the service manager."""
        self.services = {}
    
    def __getattr__(self, name):
        """Return a created service if found."""
        service = self.services.get(name)
        if service:
            return service()
        
        raise AttributeError("attribute {} not found".format(
                repr(name)))
    
    def register(self, name, service):
        """Register a service in the service manager;"""
        self.services[name] = service
    
    def register_defaults(self):
        """Register the default services."""
        for service in defaults:
            self.register(service.name, service)
