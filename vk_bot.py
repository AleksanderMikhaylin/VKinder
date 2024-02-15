from VKinder.handler.handlers import FallbackHandler, FarewellHandler, GreetingsHandler, SearchHandler, CandidatsHandler
from VKinder.model.tables import User
from handler.question.questions import TokenQuestion

class VkBot:

    def __init__(self, user_id, vk_group_client, db_session):
        self.user_id = user_id
        self.db_session = db_session
        self.first_handlers = [
            GreetingsHandler(user_id, vk_group_client),
            FarewellHandler(user_id, vk_group_client),
        ]
        self.handlers = [
            TokenQuestion(user_id, vk_group_client, db_session),
            SearchHandler(user_id, vk_group_client, db_session),
            CandidatsHandler(user_id, vk_group_client, db_session),
            # GreetingsHandler(user_id, vk_group_client),
            # FarewellHandler(user_id, vk_group_client),
            FallbackHandler(user_id, vk_group_client),
        ]
        self.last_handler = None
        self.create_user_if_not_exists()

    def create_user_if_not_exists(self):
        exists = self.db_session.query(User).filter(User.id == self.user_id).first()
        if not exists:
            self.db_session.add(User(id=self.user_id))
            self.db_session.commit()

    def handle_new_message(self, message):
        for handler in self.first_handlers:
            handler_message = handler.handle(message)
            if handler_message.get('status', True):
                # self.last_handler = handler
                for handler in self.handlers:
                    if hasattr(handler, 'candidates') :
                        handler.reset()
                return

        self_last_handler = self.last_handler
        if self_last_handler is not None:
            self_last_handler_is_active = self.last_handler.is_active()
            if self_last_handler_is_active:
                last_handler_message = self.last_handler.handle(message)
                if last_handler_message.get('status', True):
                    # self.last_handler = None
                    return
                message = last_handler_message.get('message', '')

        for handler in self.handlers:
            if hasattr(handler, 'candidates') and hasattr(self.last_handler, 'candidates'):
                handler.candidates = self.last_handler.candidates.copy()
            handler_message = handler.handle(message)
            if handler_message.get('status', True):
                self.last_handler = handler
                break
            if hasattr(handler, 'candidates'):
                self.last_handler = handler
            message = handler_message.get('message', '')
