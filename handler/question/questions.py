from VKinder.handler.question.base_question import BaseQuestion, QuestionState

from VKinder.model.tables import User
import re

CLIENT_ID = '6287487'
AUTH_LINK = 'https://oauth.vk.com/authorize?client_id=' + CLIENT_ID + '&scope=1073737727&redirect_uri=https://oauth.vk.com/blank.html&display=page&response_type=token&revoke=1'

class TokenQuestion(BaseQuestion):
    def __init__(self, user_id, vk_group_client, db_session):
        self.db_session = db_session
        super().__init__(user_id, vk_group_client)

    def question(self):
        return 'Напишите ваш токен. Токен можно получить по этой ссылке: ' + AUTH_LINK

    def is_valid_answer(self, answer, params):
        answer_bool = re.match('^[A-Za-z]\S*$', answer) is not None

        return answer_bool

    def should_ask(self):
        user = self.db_session.query(User).filter(User.id == self.user_id).first()
        return super().should_ask() and not user.token

    def handle_answer(self, answer, params):

        token = answer
        ls_token = token.split('vk1')
        if len(ls_token) == 2:
            token = 'vk1' + ls_token[1]
            ls_token = token.split('&')
            if len(ls_token) > 0:
                token = ls_token[0]

        is_valid = self.is_valid_answer(token, params)
        if is_valid:
            self.state = QuestionState.FULFILLED
            user = self.get_user()
            user.token = token

        return is_valid

    def get_user(self):
        return self.db_session.query(User).filter(User.id == self.user_id).first()


class AgeFromQuestion(BaseQuestion):
    def question(self):
        return 'Укажите минимальный возраст: '

    def is_valid_answer(self, answer, params):
        try:
            answer = int(answer)
            return 13 <= answer <= 100
        except ValueError:
            return False

    def get_param_name(self):
        return 'age_from'


class AgeToQuestion(BaseQuestion):
    def question(self):
        return 'Укажите максимальный возраст: '

    def is_valid_answer(self, answer, params):
        try:
            answer = int(answer)
            return 13 <= answer <= 100 and int(params['age_from']) <= answer
        except ValueError:
            return False

    def get_param_name(self):
        return 'age_to'


class HometownQuestion(BaseQuestion):
    def question(self):
        return 'Город рождения: '

    def is_valid_answer(self, answer, params):
        return True

    def get_param_name(self):
        return 'hometown'


class SexQuestion(BaseQuestion):
    def question(self):
        return 'Введите пол человека(1-ж, 2-м, 0-любой)'

    def is_valid_answer(self, answer, params):
        try:
            answer = int(answer)
            return answer in [1, 2, 0,]
        except ValueError:
            return False

    def get_param_name(self):
        return 'sex'


class StatusQuestion(BaseQuestion):
    def question(self):
        return 'Выберите семейное положение (1-не женат(незамужем),' \
               '2-всречается, 3-помолвлен(а), 4-женат(замужем), 5-все сложно,' \
               ' 6-в поисках, 7-в любви): '

    def is_valid_answer(self, answer, params):
        try:
            answer = int(answer)
            return 1 <= answer <= 7
        except ValueError:
            return False

    def get_param_name(self):
        return 'status'