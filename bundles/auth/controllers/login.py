from ext.aboard.controller import Controller
from bundles.auth.models.user import User

class Login(Controller):
    
    def login(self):
        return self.render("auth.login.login")
    
    def do_login(self, username=None, password=None):
        if not username or not password:
            return "Empty username or password."
        
        user = None
        for u in User.get_all():
            if u.username == username:
                user = u
                break
        
        if user is None:
            return "Invalid username."
        
        if user.check_password(password):
            self.server.services.authentication.authenticate(self.request, user)
            return "Logged in."
        else:
            return "Invalid password."
