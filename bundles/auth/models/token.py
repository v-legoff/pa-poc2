import hashlib
import random
import string

from ext.aboard.model import *

class Token(Model):
    
    """A token model."""
    
    id = None
    user = Integer()
    value = String(pkey=True)
    timestamp = Integer()
    
    def set_value(self):
        """Randomly set the value."""
        value = str(self.user) + "_" + str(self.timestamp)
        len_rand = random.randint(20, 40)
        to_pick = string.digits + string.ascii_letters + \
                "_-+^$"
        for i in range(len_rand):
            value += random.choice(to_pick)
        
        print("Private value", value)
        # Hash the value
        hashed = hashlib.sha512(value.encode())
        self.value = hashed.hexdigest()
        print("Public value", self.value)
