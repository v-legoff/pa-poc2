from ext.aboard.model import *

class User(Model):
    
    """A user model to test model and controller interaction."""
    
    username = String()
    password = String(default="not_specified")
    
    def __repr__(self):
        return "<user id={}, name={}>".format(self.id, repr(self.username))
