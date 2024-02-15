from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from VKinder.pwd import USER, PASSWORD, GROUP_TOKEN

keyboard = VkKeyboard(one_time=False)
keyboard.add_button('Назад', VkKeyboardColor.PRIMARY)
keyboard.add_button('Запомнить', VkKeyboardColor.POSITIVE)
keyboard.add_button('Дальше', VkKeyboardColor.PRIMARY)
keyboard.add_line()
keyboard.add_button('Новый поиск', VkKeyboardColor.SECONDARY)
keyboard.add_button('Выход', VkKeyboardColor.SECONDARY)
KEYBOARD_LIKE = keyboard.get_keyboard()

keyboard = VkKeyboard(one_time=False)
keyboard.add_button('Назад', VkKeyboardColor.PRIMARY)
keyboard.add_button('Запомнить', VkKeyboardColor.POSITIVE)
keyboard.add_button('Показать еще 10', VkKeyboardColor.PRIMARY)
keyboard.add_line()
keyboard.add_button('Новый поиск', VkKeyboardColor.SECONDARY)
keyboard.add_button('Выход', VkKeyboardColor.SECONDARY)
KEYBOARD_LIKE_10 = keyboard.get_keyboard()

keyboard = VkKeyboard(one_time=False)
keyboard.add_button('Назад', VkKeyboardColor.PRIMARY)
keyboard.add_button('Забыть', VkKeyboardColor.NEGATIVE)
keyboard.add_button('Дальше', VkKeyboardColor.PRIMARY)
keyboard.add_line()
keyboard.add_button('Новый поиск', VkKeyboardColor.SECONDARY)
keyboard.add_button('Выход', VkKeyboardColor.SECONDARY)
KEYBOARD_UNLIKE = keyboard.get_keyboard()

keyboard = VkKeyboard(one_time=False)
keyboard.add_button('Назад', VkKeyboardColor.PRIMARY)
keyboard.add_button('Забыть', VkKeyboardColor.NEGATIVE)
keyboard.add_button('Показать еще 10', VkKeyboardColor.PRIMARY)
keyboard.add_line()
keyboard.add_button('Новый поиск', VkKeyboardColor.SECONDARY)
keyboard.add_button('Выход', VkKeyboardColor.SECONDARY)
KEYBOARD_UNLIKE_10 = keyboard.get_keyboard()

keyboard = VkKeyboard(one_time=False)
keyboard.add_button('Новый поиск', VkKeyboardColor.SECONDARY)
keyboard.add_button('Выход', VkKeyboardColor.SECONDARY)
KEYBOARD_EMPTY = keyboard.get_keyboard()

POSTGRES_SECRET = {
    'name_db': 'vk_api_db',
    'user': USER,
    'pass': PASSWORD,
}
