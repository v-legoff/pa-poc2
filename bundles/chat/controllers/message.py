from ext.aboard.controller import Controller

class Message(Controller):
    
    def list(self, last=None):
        """Return the list of messages."""
        Message = self.server.get_model("chat.Message")
        o_messages = Message.get_all()
        messages = []
        for msg in o_messages:
            messages.append(msg.display_representation(
                ["id", "pseudo", "content"]))
        if last and last.isdigit():
            last = int(last)
            messages = [msg for msg in messages if msg["id"] > last]
        
        return self.render("chat.message.list", messages=messages)
    
    @Controller.model_id("chat.Message")
    def view(self, message):
        message = message.display_representation(
                ["id", "pseudo", "content"])
        return self.render("chat.message.view", message=message)
    
    def create(self, pseudo=None, content=None):
        """Create a message."""
        if not pseudo or not content:
            return "not valid"
        
        Message = self.server.get_model("chat.Message")
        message = Message(pseudo=pseudo, content=content)
        return "ok"
