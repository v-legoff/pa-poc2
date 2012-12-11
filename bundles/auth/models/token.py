import hashlib
import random
import string

from ext.aboard.model import *

def set_value(token):
    """Randomly create and return a value."""
    value = str(token.user) + "_" + str(token.timestamp)
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

class Token(Model):
    
    """A token model."""
    
    id = None
    user = Integer()
    timestamp = Integer()
    value = String(pkey=True, default=set_value)
