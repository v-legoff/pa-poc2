from ext.aboard.service.default import AuthenticationService

class Authentication(AuthenticationService):
    
    def __init__(self):
        AuthenticationService.__init__(self)
        self.user_model = "auth.User"
        self.token_model = "auth.Token"
