from ext.aboard.controller import Controller
from bundles.main.models.user import User

class Users(Controller):
    
    def list(self):
        return self.render("main.user.list", users=User.get_all())
    
    @Controller.model_id("main.User")
    def view(self, user):
        user = user.display_representation(["id", "username"])
        return self.render("main.user.view", user=user)
    
    def create(self):
        """Create a user."""
        user = User(username="Donald")
        user = user.display_representation(["id", "username"])
        return self.render("main.user.view", user=user)
    
    @Controller.model_id("main.User")
    def update(self, user, username=None, password=None):
        if username:
            user.username = username
        if password:
            user.password = password
        return str(user)
