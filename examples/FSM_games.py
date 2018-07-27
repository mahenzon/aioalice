import random
import logging

from aiohttp import web
from aioalice import Dispatcher, get_new_configured_app, types
from aioalice.dispatcher import MemoryStorage
from aioalice.utils.helper import Helper, HelperMode, Item


WEBHOOK_URL_PATH = '/my-alice-webhook/'  # webhook endpoint

WEBAPP_HOST = 'localhost'
WEBAPP_PORT = 3001


logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO)

# Создаем экземпляр диспетчера и подключаем хранилище в памяти
dp = Dispatcher(storage=MemoryStorage())


CANCEL_TEXTS = ['отмени', 'прекрати', 'выйти', 'выход']
GAMES_LIST = ['Угадай число', 'Наперстки']
THIMBLE = '⚫'


# Можно использовать класс Helper для хранения списка состояний
class GameStates(Helper):
    mode = HelperMode.snake_case

    SELECT_GAME = Item()  # = select_game
    GUESS_NUM = Item()  # = guess_num
    THIMBLES = Item()  # = thimbles


def gen_thimbles():
    # Генерируем массив из 3 кнопок
    # Первый аргумент - юникод символ черного кружочка
    # Аргумент по ключевому слову payload может содержать произвольный JSON
    buttons = [types.Button(THIMBLE, payload={'win': False}) for _ in range(3)]
    # Делаем первую кнопку выигрышной
    buttons[0].payload['win'] = True
    # Смешиваем кнопки
    random.shuffle(buttons)
    logging.info(f'Thimbles are: {buttons}')
    return buttons


async def get_number_from_data(user_id):
    data = await dp.storage.get_data(user_id)
    return data.get('num')


'''
Дальше хэндлеры расположены по предпочтительности срабатывания
Общение пользователя с Алисой будет ходить по хэндлерам в зависимости
от состояния. Будет отрабатывать первый подходящий хэндлер
'''


# Если текст команды содержит одно из слов отмены,
# возвращаемся в "главное меню"
@dp.request_handler(contains=CANCEL_TEXTS)
async def cancel_operation(alice_request):
    user_id = alice_request.session.user_id
    await dp.storage.reset_state(user_id)
    return alice_request.response('Хорошо, прекращаем.')


# Создаем функцию обработчик команды, которая сработает,
# если во время игры в "угадай число" отправлено число
async def user_guesses_number(alice_request):
    user_id = alice_request.session.user_id
    my_num = await get_number_from_data(user_id)
    num = int(alice_request.request.command)
    buttons = None
    if num == my_num:
        await dp.storage.reset_state(user_id)
        text = 'Верно! Молодец!'
    else:
        text = 'Нет, но ты близко! Пробуй ещё.\nЗагаданное число '
        if my_num > num:
            text += 'больше'
        else:
            text += 'меньше'
        buttons = ['Сдаюсь', 'Прекратить']
    return alice_request.response(text, buttons=buttons)


# Регистрируем обработчик не через декоратор (результат не отличается)
# Проверяем, что состояние - игра "Угадай число", а команда может быть преобразована в число
dp.register_request_handler(
    user_guesses_number,
    state=GameStates.GUESS_NUM,
    func=lambda areq: areq.request.command.isdigit()
)


# Отработает, если во время игры в угадай число
# пользовател написал команду, содержащую слово "сдаюсь"
@dp.request_handler(state=GameStates.GUESS_NUM, contains='сдаюсь')
async def user_loses_tell_number(alice_request):
    user_id = alice_request.session.user_id
    await dp.storage.reset_state(user_id)
    my_num = await get_number_from_data(user_id)
    return alice_request.response(f'А ведь ты почти угадал!\nЧисло было {my_num}')


# Регистрируем хэндлер, срабатывающий во время игры "Угадай число"
# если не сработали хэндлеры выше - команда не является числом,
# или текст не содержит слово "сдаюсь"
@dp.request_handler(state=GameStates.GUESS_NUM)
async def game_number_command_not_digit(alice_request):
    return alice_request.response(
        'Это не число! Можешь продолжить угадывать'
        ' число или попроси меня прекратить',
        buttons=['Прекратить']
    )


# Этот хэндлер сработает только если нажата кнопка во время игры в наперстки
# Тип запроса "SimpleUtterance" это не только голосовой ввод,
# но и нажатие кнопки без payload. "ButtonPressed" — нажатие кнопки с payload
@dp.request_handler(state=GameStates.THIMBLES, request_type=types.RequestType.BUTTON_PRESSED)
async def check_if_winning_button_pressed(alice_request):
    # Не смотря на то, что данный тип запроса может быть только с payload
    # проверяем, что он существует, вдруг изменится апи
    # по умолчанию payload = None
    if alice_request.request.payload and alice_request.request.payload['win']:
        text = 'Верно! Ты молодец!'
    else:
        text = 'Неа :( Давай ещё!'
    text += '\nКручу, верчу! Где?'
    return alice_request.response(text, buttons=gen_thimbles())


# Отрабатываем, если во время игры в наперстки отправлен текст, а не нажата кнопка
# Можно было бы сделать request_type=types.RequestType.SIMPLE_UTTERANCE,
# но так как варианта всего два, а первый был бы отработан выше, то это не нужно
@dp.request_handler(state=GameStates.THIMBLES)
async def thimbles_not_button(alice_request):
    return alice_request.response(
        'В этой игре нужно нажимать кнопки. '
        'Если хочешь прекратить, так и скажи',
        buttons=['Прекратить']
    )


# Если состояние "SELECT_GAME" (!) _И_ (!) при этом
# текст содержит название одной из игр - хэндлер отработает
@dp.request_handler(state=GameStates.SELECT_GAME, contains=GAMES_LIST)
async def selecting_game(alice_request):
    user_id = alice_request.session.user_id
    text = 'Отлично! Играем в '
    buttons = None
    if 'угадай число' in alice_request.request.command.lower():
        new_state = GameStates.GUESS_NUM
        text += '"Угадай число"!\nЯ загадала число от 1 до 100, угадывай!'
        # Загадываем число от 1 до 100 и запоминаем
        new_num = random.randint(1, 100)
        await dp.storage.update_data(user_id, num=new_num)
        logging.info(f'Num for {user_id} is {new_num}')
    else:
        new_state = GameStates.THIMBLES
        text += 'наперстки!\nКручу, верчу, запутать хочу!\nГде?'
        buttons = gen_thimbles()
    # Устанавливаем новое состояние - выбранная игра
    await dp.storage.set_state(user_id, new_state)
    return alice_request.response(text, buttons=buttons)


# Если состояние "SELECT_GAME"
# Хэндлер отработает только если фильтры хэндлера выше не ок
@dp.request_handler(state=GameStates.SELECT_GAME)
async def select_game_not_in_list(alice_request):
    return alice_request.response(
        'Я ещё не знаю такой игры :(\nВыбери одну из списка!',
        buttons=GAMES_LIST
    )


# Приветствуем пользователя и предлагаем сыграть в игру
# В этот хэндлер будут попадать любые команды,
# не отработанные хэндлерами выше. это - "главное меню"
@dp.request_handler()
async def handle_any_request(alice_request):
    user_id = alice_request.session.user_id
    # Устанавливаем состояние пользователя "выбор игры"
    await dp.storage.set_state(user_id, GameStates.SELECT_GAME)

    text = 'Давай играть! Выбери игру:'
    # Если сессия новая, приветствуем пользователя
    if alice_request.session.new:
        text = 'Привет! ' + text
    # Предлагаем пользователю список игр
    return alice_request.response(text, buttons=GAMES_LIST)


if __name__ == '__main__':
    app = get_new_configured_app(dispatcher=dp, path=WEBHOOK_URL_PATH)
    web.run_app(app, host=WEBAPP_HOST, port=WEBAPP_PORT)
