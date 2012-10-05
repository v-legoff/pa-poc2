from ext.aboard.controller import Controller
from bundles.main.models.user import User

class Users(Controller):
    
    def list(self):
        print(self.request)
        return str(User.get_all())
    
    @Controller.model_id("main.User")
    def view(self, *args, **kwargs):
        print("view", args, kwargs)
        return "ok"
    
    def create(self):
        """Create a user."""
        user = User(username="Donald")
        return str(user)
