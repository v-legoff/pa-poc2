import hashlib
import random
import string

from ext.aboard.model import *

class User(Model):
    
    """A user model, which stores authentication informations."""
    
    username = String()
    password = String() #  the hashed password
    salt = String()
    
    def __repr__(self):
        return "<user id={}, name={}>".format(self.id, repr(self.username))
    
    @staticmethod
    def hash_password(password, hash_alg):
        """Returh the hashed password as hexdigest, given the algorithm."""
        hash = hashlib.new(hash_alg, password.encode())
        return hash.hexdigest()
    
    @staticmethod
    def generate_salt(min=6, max=15):
        """Generate a salt randomly."""
        len_salt = random.randint(min, max)
        to_pick = string.digits + string.ascii_letters + \
                "_-+^$"
        salt = ""
        for i in range(len_salt):
            salt += random.choice(to_pick)
        
        print("Generated salt:", salt)
        return salt
    
    def update_password(self, password, hash_alg="sha1"):
        """Hash and store the hexdigest of the specified password."""
        hashed_password = self.hash_password(password, hash_alg)
        self.password = hashed_password
    
    def check_password(self, password, hash_alg="sha1"):
        """Return whether the password is correct."""
        hashed_password = self.hash_password(password, hash_alg)
        return self.password == hashed_password
