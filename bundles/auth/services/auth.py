from ext.aboard.service import Service

class Auth(Service):
    
    def authenticate(self, request, user):
        print("Authenticate")
