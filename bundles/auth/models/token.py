import hashlib
import random
import string

from ext.aboard.model import *

class Token(Model):
    
    """A token model."""
    
    id = None
    user = Integer()
    timestamp = Integer()
    value = String(pkey=True)
    
    def __init__(self, user=None, timestamp=None):
        value = None
        if user and timestamp:
            value = Token.get_token_value(user, timestamp)
        
        Model.__init__(self, user=user, timestamp=timestamp, value=value)
    
    @staticmethod
    def get_token_value(user, timestamp):
        """Randomly create and return a token value."""
        value = str(user) + "_" + str(timestamp)
        len_rand = random.randint(20, 40)
        to_pick = string.digits + string.ascii_letters + \
                "_-+^$"
        for i in range(len_rand):
            value += random.choice(to_pick)
        
        print("Private value", value)
        
        # Hash the value
        hashed = hashlib.sha512(value.encode())
        value = hashed.hexdigest()
        print("Public value", value)
        return value
