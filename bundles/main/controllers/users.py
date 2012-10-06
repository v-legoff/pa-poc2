from ext.aboard.controller import Controller
from bundles.main.models.user import User

class Users(Controller):
    
    def list(self):
        print(self.request)
        return str(User.get_all())
    
    @Controller.model_id("main.User")
    def view(self, user):
        return str(user)
    
    def create(self):
        """Create a user."""
        user = User(username="Donald")
        return str(user)
    
    @Controller.model_id("main.User")
    def update(self, user, username=None, password=None):
        if username:
            user.username = username
        if password:
            user.password = password
        return str(user)
