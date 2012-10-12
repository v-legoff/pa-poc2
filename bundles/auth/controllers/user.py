from ext.aboard.controller import Controller
from bundles.auth.models.user import User as ModUser

class User(Controller):
    
    def list(self):
        """Return the list of users."""
        print(self.server.services.authentication.authenticated(self.request))
        return self.render("auth.user.list", users=ModUser.get_all())
    
    @Controller.model_id("auth.User")
    def view(self, user):
        user = user.display_representation(["id", "username"])
        return self.render("auth.user.view", user=user)
    
    def new(self):
        return self.render("auth.user.new")
    
    def create(self, username=None, password=None):
        """Create a user."""
        infos = {}
        if username:
            infos["username"] = username
        if password:
            infos["password"] = ModUser.hash_password(password, "sha1")
        infos["salt"] = ModUser.generate_salt()
        user = ModUser(**infos)
        user = user.display_representation(["id", "username"])
        return self.render("auth.user.view", user=user)
    
    @Controller.model_id("auth.User")
    def edit(self, user):
        user = user.display_representation(["id", "username"])
        return self.render("auth.user.update", user=user)
    
    @Controller.model_id("auth.User")
    def update(self, user, username=None, password=None):
        if username:
            user.username = username
        if password:
            user.update_password(password)
        user = user.display_representation(["id", "username"])
        return self.render("auth.user.view", user=user)
    
    @Controller.model_id("auth.User")
    def delete(self, user):
        user.delete()
        raise cherrypy.HTTPRedirect("/users")
