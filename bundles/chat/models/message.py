from ext.aboard.model import *

class Message(Model):
    
    """A message model."""
    
    pseudo = String()
    content = String()
