from random import randrange

class MessageSender:

    def __init__(self, user_id, vk_group_client):
        self.vk_group_client = vk_group_client
        self.user_id = user_id

    def write_msg(self, message):
        self.vk_group_client.method('messages.send', {'user_id': self.user_id, 'message': message, 'random_id': randrange(10 ** 7)})