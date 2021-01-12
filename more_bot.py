# импорт дополнительных модулей
import logging
import random
import TenGiphPy

from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import text, hcode
from aiogram.types import ParseMode, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton

from settings import API_TOKEN, TENOR_TOKEN
from mongodb import db_send_compliment, get_compliment, db_send_error, get_error

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# обработчик команд админа
@dp.message_handler(commands=['admin_more'])
async def admin_commands(msg: types.Message):
    await msg.answer('/compliment_list\n/error_list')

@dp.message_handler(commands=['compliment_list'])
async def admin_compliment_list(msg: types.Message):
    await msg.answer(get_compliment)

@dp.message_handler(commands=['error_list'])
async def admin_error_list(msg: types.Message):
    await msg.answer(get_error)

# обработчик команды start
@dp.message_handler(commands=['start'])
async def welcome(msg: types.Message):
    key_compliment = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('Можно комплимент?'))
    await msg.answer(text('Привет!\n\n- отправьте русский текст в английской раскладке и бот изменит его в русскую раскладку и наоборот', 
        '\n\n- отправьте ', hcode('Можно комплимент?'), 'и бот скажет вам доброе слово', 
        '\n\n- вы так же можете отправлять свои комплименты с помощью /send_compliment', 
        '\n\n- отправьте слово в начале которого будет #, чтобы найти такую гифку', 
        '\n\nЕсли что-то непонятно, отправьте /help', 
        '\n\nЕсли произошла какая-то ошибка, сообщите о ней с помощью /send_error'), parse_mode=ParseMode.HTML, reply_markup=key_compliment)

@dp.message_handler(commands=['help'])
async def help(msg: types.Message):
    await msg.answer(text('- например, если вы отправили ', hcode('rfr ltkf&'), '\nто бот изменит это на ', hcode('как дела?'), 
        '\nи наоборот, если вы отправили ', hcode('как дела?'), '\nоно будет изменено на ', hcode('rfr ltkf&'), 
        '\n\n- комплименты беруться из готового списка', 
        '\n\n- например, если вы отправили ', hcode('#котики'), ', то бот отправит рандомную гифку по этому запросу'), parse_mode=ParseMode.HTML)

# отправка комплиментов в базу данных
@dp.message_handler(commands=['send_compliment'])
async def send_compliment(msg: types.Message):
    if msg.text == '/send_compliment':
        await msg.answer('Пожалуйста, сначала зажмите\n/send_compliment  и ниже, в этом же сообщении, напишите ваш комплимент')
    else:
        await msg.answer('Ваш комплимент скоро будет добален, большое спасибо!')
        delete_list = {'s': '', 'e': '', 'n': '', 'd': '', 'c': '', 'o': '', 'm': '', 'p': '', 'l': '', 'i': '', 't': '', '/': '', '_': ''}
        compliment_text = ''.join(delete_list.get(ch, ch) for ch in msg.text)
        db_send_compliment(compliment_text)

# отправка ошибок в базу данных
@dp.message_handler(commands=['send_error'])
async def send_error(msg: types.Message):
    if msg.text == '/send_error':
        await msg.answer('Пожалуйста, сначала зажмите\n/send_error  и ниже, в этом же сообщении, опишите случившуюся ошибку')
    else:
        await msg.answer('Ваша ошибка скоро будет исправлена')
        delete_list = {'s': '', 'e': '', 'n': '', 'd': '', 'r': '', 'o': '', '/': '', '_': ''}
        error_text = ''.join(delete_list.get(ch, ch) for ch in msg.text)
        db_send_error(error_text)

@dp.message_handler(content_types=['text'])
async def echo(msg: types.Message):
    delete_list = {'#': ''}
    gif_text = ''.join(delete_list.get(ch, ch) for ch in msg.text)
    # отправка комплимента
    if (msg.text).lower() == 'можно комплимент?':
        await msg.answer(random.choice(get_compliment))
    # отправка гифки
    elif msg.text == '#' + gif_text:
        try:
            tenor = TenGiphPy.Tenor(TENOR_TOKEN)
            await msg.answer(tenor.random(gif_text))
        except Exception:
            await msg.answer('По вашему запросу ничего не удалось найти(')
    # изменение раскладки
    else:
        layout_list = {'й': 'q', 'ц': 'w', 'у': 'e', 'к': 'r', 'е': 't', 'н': 'y', 'г': 'u', 'ш': 'i', 'щ': 'o', 'з': 'p', 'х': '[', 
            'ъ': ']', 'ф': 'a', 'ы': 's', 'в': 'd', 'а': 'f', 'п': 'g', 'р': 'h', 'о': 'j', 'л': 'k', 'д': 'l', 'ж': ';', 'э': "'", 'я': 'z', 
            'ч': 'x', 'с': 'c', 'м': 'v', 'и': 'b', 'т': 'n', 'ь': 'm', 'б': ',', 'ю': '.', 'ё': '`', 'Й': 'Q', 'Ц': 'W', 'У': 'E', 'К': 'R', 
            'Е': 'T', 'Н': 'Y', 'Г': 'U', 'Ш': 'I', 'Щ': 'O', 'З': 'P', 'Х': '{', 'Ъ': '}', 'Ф': 'A', 'Ы': 'S', 'В': 'D', 'А': 'F', 'П': 'G', 
            'Р': 'H', 'О': 'J', 'Л': 'K', 'Д': 'L', 'Ж': ':', 'Э': '"', 'Я': 'Z', 'Ч': 'X', 'С': 'C', 'М': 'V', 'И': 'B', 'Т': 'N', 'Ь': 'M', 
            'Б': '<', 'Ю': '>', 'Ё': '~'}
        layout_text = ''.join(layout_list.get(ch, ch) for ch in msg.text)
        if layout_text != msg.text:
            en_layout_list = {'й': 'q', 'ц': 'w', 'у': 'e', 'к': 'r', 'е': 't', 'н': 'y', 'г': 'u', 'ш': 'i', 'щ': 'o', 'з': 'p', 'х': '[', 
                'ъ': ']', 'ф': 'a', 'ы': 's', 'в': 'd', 'а': 'f', 'п': 'g', 'р': 'h', 'о': 'j', 'л': 'k', 'д': 'l', 'ж': ';', 'э': "'", 'я': 'z', 
                'ч': 'x', 'с': 'c', 'м': 'v', 'и': 'b', 'т': 'n', 'ь': 'm', 'б': ',', 'ю': '.', '.': '/', 'ё': '`', 'Й': 'Q', 'Ц': 'W', 'У': 'E', 
                'К': 'R', 'Е': 'T', 'Н': 'Y', 'Г': 'U', 'Ш': 'I', 'Щ': 'O', 'З': 'P', 'Х': '{', 'Ъ': '}', 'Ф': 'A', 'Ы': 'S', 'В': 'D', 'А': 'F', 
                'П': 'G', 'Р': 'H', 'О': 'J', 'Л': 'K', 'Д': 'L', 'Ж': ':', 'Э': '"', 'Я': 'Z', 'Ч': 'X', 'С': 'C', 'М': 'V', 'И': 'B', 'Т': 'N', 
                'Ь': 'M', 'Б': '<', 'Ю': '>', ',': '?', 'Ё': '~', '"': '@', ';': '$', ':': '^', '?': '&'}
            layout_text = ''.join(en_layout_list.get(ch, ch) for ch in msg.text)
            await msg.answer(text(hcode(layout_text)), parse_mode=ParseMode.HTML)
        else:
            ru_layout_list = {'q': 'й', 'w': 'ц', 'e': 'у', 'r': 'к', 't': 'е', 'y': 'н', 'u': 'г', 'i': 'ш', 'o': 'щ', 'p': 'з', '[': 'х', 
                ']': 'ъ', 'a': 'ф', 's': 'ы', 'd': 'в', 'f': 'а', 'g': 'п', 'h': 'р', 'j': 'о', 'k': 'л', 'l': 'д', ';': 'ж', "'": 'э', 'z': 'я', 
                'x': 'ч', 'c': 'с', 'v': 'м', 'b': 'и', 'n': 'т', 'm': 'ь', ',': 'б', '.': 'ю', '/': '.', '`': 'ё', 'Q': 'Й', 'W': 'Ц', 'E': 'У', 
                'R': 'К', 'T': 'Е', 'Y': 'Н', 'U': 'Г', 'I': 'Ш', 'O': 'Щ', 'P': 'З', '{': 'Х', '}': 'Ъ', 'A': 'Ф', 'S': 'Ы', 'D': 'В', 'F': 'А', 
                'G': 'П', 'H': 'Р', 'J': 'О', 'K': 'Л', 'L': 'Д', ':': 'Ж', '"': 'Э', 'Z': 'Я', 'X': 'Ч', 'C': 'С', 'V': 'М', 'B': 'И', 'N': 'Т', 
                'M': 'Ь', '<': 'Б', '>': 'Ю', '?': ',', '~': 'Ё', '@': '"', '$': ';', '^': ':', '&': '?'}
            layout_text = ''.join(ru_layout_list.get(ch, ch) for ch in msg.text)
            await msg.answer(text(hcode(layout_text)), parse_mode=ParseMode.HTML)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
