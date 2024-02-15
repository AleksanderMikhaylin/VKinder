from random import randrange
from VKinder.handler.base_handler import BaseHandler
from VKinder.handler.question.questions import AgeFromQuestion, AgeToQuestion, HometownQuestion, SexQuestion, \
    StatusQuestion, TokenQuestion
from VKinder.model.tables import User, Candidate, Photo, CandidatesForUser, ReviewedCandidates
from vk_api import VkApi
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from VKinder.settings import KEYBOARD_LIKE, KEYBOARD_LIKE_10, KEYBOARD_UNLIKE, KEYBOARD_UNLIKE_10, KEYBOARD_EMPTY


class GreetingsHandler(BaseHandler):

    def keywords(self):
        return ['Привет', 'Hello', 'VKinder', 'ВКиндер']

    def handle_impl(self, _message):
        # keyboard = VkKeyboard(one_time=True)
        # keyboard.add_button('Назад', VkKeyboardColor.POSITIVE)
        # keyboard.add_button('Вперед', VkKeyboardColor.POSITIVE)

        self.write_msg(f'Добро пожаловать в VKinder!\n'
                       'Сервис предназначенный для романтических знакомств в соответствии с заданными параметрами '
                       '(возраст, пол, город, семейное положение) и с учётом геолокации.\n'
                       'Напишите "Старт" для начала работы',
                       )
        return {
            'status': True,
            'message': '',
        }


class FarewellHandler(BaseHandler):

    def keywords(self):
        return ['Пока', 'Выход', 'Bye']

    def handle_impl(self, _message):
        self.write_msg(f'Грустно видеть, как ты уходишь :(\nПока!')
        return {
            'status': True,
            'message': '',
        }


class SearchHandler(BaseHandler):

    def __init__(self, user_id, vk_group_client, db_session):
        self.questions = []
        self.search_params = {}
        self.search_completed = False
        self.vk_user_client = None
        self.db_session = db_session
        self.candidates = []
        super().__init__(user_id, vk_group_client)

    def reset(self):
        self.search_params = {}
        self.search_completed = False
        self.questions = [
            AgeFromQuestion(self.user_id, self.vk_group_client),
            AgeToQuestion(self.user_id, self.vk_group_client),
            HometownQuestion(self.user_id, self.vk_group_client),
            SexQuestion(self.user_id, self.vk_group_client),
            StatusQuestion(self.user_id, self.vk_group_client),
            TokenQuestion(self.user_id, self.vk_group_client, self.db_session),
        ]

    def keywords(self):
        return ['Старт', 'Start', 'Новый поиск', 'Продолжить поиск']

    def is_active(self):
        if len(self.candidates) > 0:
            return False

        for question in self.questions:
            if question.should_handle_answer():
                return True
        return False

    def handle_impl(self, message):
        if not self.search_completed and len(self.questions) == 0 and len(self.search_params) > 0:
            new_message = self.find_match()
            return {
                'status': False,
                'message': new_message,
            }

        if self.should_handle(message):
            self.reset()

        question = self.questions[0]
        if question.should_handle_answer():
            if not question.handle_answer(message, self.search_params):
                question.ask()
            else:
                self.questions.pop(0)

        while len(self.questions) > 0 and not self.is_active():
            question = self.questions[0]
            if question.should_ask():
                question.ask()
            else:
                self.questions.pop(0)

        if len(self.questions) == 0:
            new_message = self.find_match()
            return {
                'status': False,
                'message': new_message,
            }
        return {
            'status': True,
            'message': '',
        }

    def find_match(self):
        user = self.db_session.query(User).filter(User.id == self.user_id).first()
        self.vk_user_client = VkApi(token=user.token)
        candidates = self.search()
        if candidates is not None:
            self.candidates = candidates
        else:
            self.write_msg(f'Не верно введен токен!')

            return 'Запрос токена'

        if len(self.candidates) == 0:
            self.write_msg(f'Никого не найдено!\n'
                           ' '
                           'Запускаю новый поиск....\n'
                           ' ',
                           )

            return 'Новый поиск'

        # self.send_candidat(self.candidates)

        for candidate in self.candidates:
            top_photos = self.get_popular_profile_photos(candidate['id'])
            candidate['top_photos'] = top_photos

        self.write_msg(f'Всего найдено {len(self.candidates)} кандидатов!')
        return 'Поиск завершен'

        # for candidate in candidates:
        #     top_photos = self.get_popular_profile_photos(candidate['id'])
        #     candidate['top_photos'] = top_photos
        #     result = f"{candidate['first_name']} {candidate['last_name']}\n"
        #     result += f"https://vk.com/{candidate['screen_name']}\n"
        #
        #     candidate_exists = self.db_session.query(Candidate).filter(Candidate.id == candidate['id']).first()
        #     if not candidate_exists:
        #         c = Candidate(
        #             id=candidate['id'],
        #             first_name=candidate['first_name'],
        #             last_name=candidate['last_name'],
        #             screen_name=candidate['screen_name'],
        #         )
        #         self.db_session.add(c)
        #         user.candidates.append(c)
        #     else:
        #         user.candidates.append(candidate_exists)
        #
        #     self.write_msg(result)
        #
        #     attachments = []
        #     for photo in top_photos:
        #         owner_photo_id = f"photo{photo['owner_id']}_{photo['id']}"
        #         attachments.append(owner_photo_id)
        #         photo_exists = self.db_session.query(Photo).filter(Photo.id == owner_photo_id).first()
        #         if not photo_exists:
        #             self.db_session.add(
        #                 Photo(
        #                     id=owner_photo_id,
        #                     photo_id=photo['id'],
        #                     candidate_id=photo['owner_id'],
        #                     likes_count=photo['likes']['count'],
        #                     comments_count=photo['comments']['count'],
        #                 )
        #             )
        #     self.send_attachment(','.join(attachments))
        #
        # self.db_session.commit()

    def send_candidat(self, candidates):
        candidate = candidates[0]
        top_photos = self.get_popular_profile_photos(candidate['id'])
        candidate['top_photos'] = top_photos
        result = f"{candidate['first_name']} {candidate['last_name']}\n"
        result += f"https://vk.com/{candidate['screen_name']}\n"

        self.write_msg(result)

        keyboard = VkKeyboard(one_time=True)
        keyboard.add_button('Назад', VkKeyboardColor.PRIMARY)
        keyboard.add_button('Лайкнуть', VkKeyboardColor.POSITIVE)
        keyboard.add_button('Пропустить', VkKeyboardColor.NEGATIVE)
        keyboard.add_button('Дальше', VkKeyboardColor.PRIMARY)

        attachments = []
        for photo in top_photos:
            owner_photo_id = f"photo{photo['owner_id']}_{photo['id']}"
            attachments.append(owner_photo_id)
        self.send_attachment(','.join(attachments), keyboard)

    def send_attachment(self, attachment, keyboard):

        self.vk_group_client.method('messages.send',
                                    {
                                        'user_id': self.user_id,
                                        'attachment': attachment,
                                        'random_id': randrange(10 ** 7),
                                        'keyboard': keyboard.get_keyboard(),
                                    })

    def get_popular_profile_photos(self, owner_id):
        response = self.vk_user_client.method('photos.get', {'owner_id': owner_id, 'album_id': 'profile', 'extended': 1,
                                                             'count': 1000})
        items = response['items']

        def sum_likes_and_comments_count(item):
            return item['likes']['count'] + item['comments']['count']

        items.sort(key=sum_likes_and_comments_count)

        most_liked_photos = items[-3:]
        return most_liked_photos

    def search(self):
        params = {'has_photo': 1, 'count': 10, 'fields': 'screen_name'}
        try:
            response = self.vk_user_client.method('users.search', {**self.search_params, **params})
        except:
            return None

        def already_matched(user_id, candidate_id):
            try:
                user = self.db_session.query(User).filter(User.id == user_id, User.candidates.any(id=candidate_id))
                # user = self.db_session.query(User).filter(User.id == user_id, User.candidates.any(id=candidate_id)).first()
                return user is not None
            except:
                return True

        # items = [item for item in response['items'] if
        #          not item['is_closed'] and not already_matched(self.user_id, item['id'])]
        self.search_completed = True
        items = [item for item in response['items']]
        return items


class CandidatsHandler(BaseHandler):

    def __init__(self, user_id, vk_group_client, db_session):
        self.vk_user_client = None
        self.db_session = db_session
        self.candidates = []
        self.current_index = 0
        super().__init__(user_id, vk_group_client)

    def reset(self):
        self.candidates = []
        self.current_index = 0

    def is_active(self):
        return len(self.candidates) > 0

    def keywords(self):
        return ['Назад', 'Запомнить', 'Забыть', 'Дальше', 'Поиск завершен']

    def handle_impl(self, _message):

        if len(self.candidates) == 0:
            self.write_msg('Список кандидатов пуст, начните новый поиск!', KEYBOARD_LIKE)
            return {
                'status': True,
                'message': '',
            }

        candidate = self.candidates[self.current_index]

        if _message.lower() == 'поиск завершен':
            self.current_index = 0
        elif _message.lower() == 'новый поиск':
            self.current_index = 0
            self.candidates = []
            return {
                'status': False,
                'message': 'Старт',
            }
        elif _message.lower() == 'выход':
            self.current_index = 0
            self.candidates = []
            return {
                'status': False,
                'message': 'Пока',
            }
        elif _message.lower() == 'назад':
            if self.current_index == 0:
                self.write_msg('Это первый кандидат по списку!', '')
                return {
                    'status': True,
                    'message': '',
                }
            self.current_index -= 1
        elif _message.lower() == 'дальше':
            if self.current_index + 1 == len(self.candidates):
                self.write_msg('Это последний кандидат по списку!', '')
                return {
                    'status': True,
                    'message': '',
                }
            self.current_index += 1
        elif _message.lower() == 'показать еще 10':
            if self.current_index + 1 == len(self.candidates):
                self.write_msg('Это последний кандидат по списку!', '')
                return {
                    'status': True,
                    'message': '',
                }
            self.current_index += 1
        elif _message.lower() == 'запомнить':

            try:
                if self.db_session.query(Candidate).get(candidate['id']) is None:
                    self.db_session.add(
                        Candidate(
                            id=candidate['id'],
                            first_name=candidate['first_name'],
                            last_name=candidate['last_name'],
                            screen_name=candidate['screen_name'],
                        ))

                if self.db_session.query(CandidatesForUser).filter(
                        CandidatesForUser.user_id == self.user_id,
                        CandidatesForUser.candidate_id == candidate['id']
                ).first() is None:
                    self.db_session.add(
                        CandidatesForUser(
                            user_id=self.user_id,
                            candidate_id=candidate['id'],
                        ))

                self.db_session.commit()
                self.write_msg('Пользователь добавлен в список избранных!', KEYBOARD_UNLIKE)
            except Exception as e:
                self.db_session.rollback()
                self.write_msg(f'Ошибка при добавлении пользователя в список избранных: {e}', KEYBOARD_LIKE)

            return {
                'status': True,
                'message': '',
            }

        elif _message.lower() == 'забыть':
            try:
                rec = self.db_session.query(CandidatesForUser).filter(
                    CandidatesForUser.user_id == self.user_id,
                    CandidatesForUser.candidate_id == candidate['id']
                ).first()

                if rec is not None:
                    self.db_session.delete(rec)
                    self.db_session.commit()
                else:
                    print('User not found')

                self.write_msg('Пользователь удален из списока избранных!', KEYBOARD_LIKE)
            except Exception as e:
                self.db_session.rollback()
                self.write_msg(f'Ошибка удаления пользователя из списока избранных: {e}', KEYBOARD_UNLIKE)

            return {
                'status': True,
                'message': '',
            }

            self.write_msg('Пользователь удален из списока избранных!', KEYBOARD_LIKE)
            return {
                'status': True,
                'message': '',
            }

        self.send_candidat()
        return {
            'status': True,
            'message': '',
        }

    def send_candidat(self):

        candidate = self.candidates[self.current_index]
        rec = self.db_session.query(CandidatesForUser).filter(
            CandidatesForUser.user_id == self.user_id,
            CandidatesForUser.candidate_id == candidate['id']
        ).first()

        if rec is not None:
            if self.current_index + 1 == len(self.candidates):
                keyboard = KEYBOARD_UNLIKE_10
            else:
                keyboard = KEYBOARD_UNLIKE
        else:
            if self.current_index + 1 == len(self.candidates):
                keyboard = KEYBOARD_LIKE_10
            else:
                keyboard = KEYBOARD_LIKE

        result = f"{candidate['first_name']} {candidate['last_name']} #{self.current_index + 1}\n"
        result += f"https://vk.com/{candidate['screen_name']}\n"

        self.write_msg(result, keyboard)

        attachments = []
        for photo in candidate['top_photos']:
            owner_photo_id = f"photo{photo['owner_id']}_{photo['id']}"
            attachments.append(owner_photo_id)

        if len(attachments) > 0:
            self.send_attachment(','.join(attachments))
        else:
            self.write_msg('К сожалению прикрепленных фото у пользователя нет... ((', keyboard)

    def send_attachment(self, attachment):

        self.vk_group_client.method('messages.send',
                                    {
                                        'user_id': self.user_id,
                                        'attachment': attachment,
                                        'random_id': randrange(10 ** 7),
                                        'keyboard': '',
                                    })


class FarewellHandler(BaseHandler):

    def keywords(self):
        return ['Пока', 'Выход', 'Bye']

    def handle_impl(self, _message):
        self.write_msg(f'Грустно видеть, как ты уходишь :(\nПока!')
        return {
            'status': True,
            'message': '',
        }


class FallbackHandler(BaseHandler):

    def should_handle(self, _message):
        return True

    def handle_impl(self, _message):
        self.write_msg('Не понимаю о чем вы... Для справки напишите "Привет"')
        return {
            'status': True,
            'message': '',
        }

