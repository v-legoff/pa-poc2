import hashlib
import re

from ext.aboard.model.exceptions import ObjectNotFound
from ext.aboard.service import Service

# Constants
RE_AUTH = re.compile(r"^(\d+)_([a-f0-9]{128})$")

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
        
        uid, signature = re_auth.groups()
        try:
            user = self.server.get_model("auth.User").find(int(uid))
        except ObjectNotFound:
            print("user not found")
            return False
        
        remote_addr = request.headers["Remote-Addr"]
        user_agent = request.headers["User-Agent"]
        to_hash = user.username + user.password + user.salt
        to_hash += remote_addr + user_agent
        digest = hashlib.sha512(to_hash.encode()).hexdigest()
        return digest == signature
    
    def authenticate(self, request, user):
        """Authenticate the user.
        
        This method registers a cookie containing informations (the user ID,
        the user hashed password, the user salt, the User-Agent, the
        Remote-Addr.
        
        """
        remote_addr = request.headers["Remote-Addr"]
        user_agent = request.headers["User-Agent"]
        to_hash = user.username + user.password + user.salt
        to_hash += remote_addr + user_agent
        digest = hashlib.sha512(to_hash.encode()).hexdigest()
        value = str(user.id) + "_" + digest
        name = "python-aboard-auth"
        self.server.set_cookie(name, value, 900)
