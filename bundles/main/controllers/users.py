from ext.aboard.controller import Controller
from bundles.main.models.user import User

class Users(Controller):
    
    def list(self):
        """Return the list of users."""
        return self.render("main.user.list", users=User.get_all())
    
    @Controller.model_id("main.User")
    def view(self, user):
        user = user.display_representation(["id", "username", "password"])
        return self.render("main.user.view", user=user)
    
    def new(self):
        return self.render("main.user.new")
    
    def create(self, username=None, password=None):
        """Create a user."""
        infos = {}
        if username:
            infos["username"] = username
        if password:
            infos["password"] = password
        user = User(**infos)
        user = user.display_representation(["id", "username",
                "password"])
        return self.render("main.user.view", user=user)
    
    @Controller.model_id("main.User")
    def update(self, user, username=None, password=None):
        if username:
            user.username = username
        if password:
            user.password = password
        user = user.display_representation(["id", "username",
                "password"])
        return self.render("main.user.view", user=user)
    
    @Controller.model_id("main.User")
    def delete(self, user):
        user.delete()
        return str("")
