from VKinder.handler.helper.message_sender import MessageSender


class BaseHandler(MessageSender):

    def keywords(self):
        return []

    def normalized_keywords(self):
        return [keyword.lower() for keyword in self.keywords()]

    def should_handle(self, message):
        return message.lower() in self.normalized_keywords()

    def is_active(self):
        return False

    def handle(self, message):
        if not self.should_handle(message) and not self.is_active():
            return False
        self.handle_impl(message)
        return True

    def handle_impl(self, message):
        pass

