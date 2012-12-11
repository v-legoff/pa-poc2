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


"""Module containing the AuthenticationService class.

This class contains the authentication service, used to keep a user
connected for a defined amount of time.

"""

import time

from ext.aboard.model.exceptions import ObjectNotFound
from ext.aboard.service import Service

class AuthenticationService(Service):
    
    """Class containing the authentication service.
    
    This service does not handle directly the login process (aka.
    the controll of the username and password).  This task should
    be handled by a controller or by a subclass of this service.  This
    service's goals are:
    *  Keep a connected user loged-in for an ammount of time
    *  Recognize a logged-in user.
    
    """
    
    def __init__(self):
        Service.__init__(self)
        self.user_model = ""
        self.token_model = ""
        self.time_expire = 900
    
    def authenticated(self, request):
        """Return whether the request is an identified user."""
        value = self.server.get_cookie("python-aboard-auth")
        if not value:
            print("no stored")
            return False
        
        try:
            Token = self.server.get_model(self.token_model)
        except KeyError:
            print("Can not find the token model.")
            return False
        
        try:
            token = Token.find(value=value)
        except ObjectNotFound:
            print("Token not found")
            return False
        
        try:
            User = self.server.get_model(self.user_model)
        except KeyError:
            print("Can not find the user model.")
            return False
        
        try:
            user = User.find(token.user)
        except ObjectNotFound:
            print("user not found")
            return False
        
        return True
    
    def authenticate(self, request, user):
        """Authenticate the user.
        
        This method:
            Create a new token
            Combine the token public value and the remote address
            Store on the client-side (cookie) the value
        
        """
        remote_addr = request.headers["Remote-Addr"]
        Token = self.server.get_model(self.token_model)
        token = Token(user=user.id, timestamp=int(time.time()))
        name = "python-aboard-auth"
        self.server.set_cookie(name, token.value, self.time_expire)
