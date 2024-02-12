from VKinder.handler.helper.message_sender import MessageSender
import enum

class QuestionState(enum.Enum):
    NOT_ASKED = 0
    ASKED = 1
    FULFILLED = 2


class BaseQuestion(MessageSender):

    def __init__(self, user_id, vk_group_client):
        self.state = QuestionState.NOT_ASKED
        super().__init__(user_id, vk_group_client)

    def question(self):
        return ''

    def is_valid_answer(self, _answer, _params):
        return True

    def get_param_name(self):
        return ''

    def should_ask(self):
        return self.state == QuestionState.NOT_ASKED

    def ask(self):
        self.state = QuestionState.ASKED
        self.write_msg(self.question())

    def should_handle_answer(self):
        return self.state == QuestionState.ASKED

    def handle_answer(self, answer, params):
        is_valid = self.is_valid_answer(answer, params)
        if is_valid:
            self.state = QuestionState.FULFILLED
            params[self.get_param_name()] = answer
        return is_valid