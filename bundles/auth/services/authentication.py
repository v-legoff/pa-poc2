import hashlib
import re
import time

from ext.aboard.model.exceptions import ObjectNotFound
from ext.aboard.service import Service

# XConstants
RE_AUTH = re.compile(r"^[0-9a-f]{128}$")

class Authentication(Service):
    
    def authenticated(self, request):
        """Return whether the request is an identified user."""
        value = self.server.get_cookie("python-aboard-auth")
        if not value:
            print("no stored")
            return False
        
        re_auth = RE_AUTH.search(value)
        if not re_auth:
            print("Regex does not match")
            return False
        
        print(value)
        try:
            token = self.server.get_model("auth.Token").find(value=value)
        except ObjectNotFound:
            print("Token not found")
            return False
        
        try:
            user = self.server.get_model("auth.User").find(token.user)
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
        Token = self.server.get_model("auth.Token")
        token = Token(user=user.id, timestamp=int(time.time()), value=".")
        token.set_value()
        name = "python-aboard-auth"
        self.server.set_cookie(name, token.value, 900)
