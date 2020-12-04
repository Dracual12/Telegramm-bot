import telebot
from telebot import types
import re
import heapq
from bs4 import BeautifulSoup
from random import choice
import requests

heads = []

stopwords = {'этой', 'ей', 'бы', 'же', 'через', 'его', 'том', 'никогда', 'хорошо', 'мой', 'ничего', 'ним', 'во',
             'совсем', 'то', 'над', 'тоже', 'этом', 'им', 'мне', 'ж', 'чтобы', 'ее', 'только', 'тут', 'была', 'один',
             'моя', 'еще', 'почти', 'всю', 'надо', 'много', 'между', 'уж', 'лучше', 'свою', 'потому', 'были', 'был',
             'меня', 'них', 'мы', 'другой', 'ну', 'не', 'тогда', 'конечно', 'кто', 'он', 'я', 'там', 'наконец',
             'больше',
             'ведь', 'эти', 'ней', 'при', 'на', 'три', 'ты', 'нее', 'было', 'себя', 'за', 'про', 'с', 'всего', 'куда',
             'какой', 'даже', 'после', 'в', 'него', 'вам', 'когда', 'или', 'будто', 'впрочем', 'нас', 'уже', 'можно',
             'они', 'такой', 'до', 'все', 'чтоб', 'но', 'вдруг', 'ни', 'их', 'по', 'чего', 'будет', 'разве', 'она',
             'вы',
             'теперь', 'может', 'к', 'тебя', 'раз', 'чем', 'себе', 'какая', 'для', 'зачем', 'хоть', 'тем', 'и', 'быть',
             'под', 'два', 'тот', 'нельзя', 'сам', 'у', 'здесь', 'ему', 'где', 'об', 'если', 'вас', 'как', 'сейчас',
             'из', 'ли', 'эту', 'вот', 'а', 'без', 'иногда', 'более', 'всегда', 'всех', 'от', 'нет', 'этот', 'что',
             'со',
             'так', 'нибудь', 'того', 'опять', 'есть', 'чуть', 'этого', 'перед', 'да', 'о', 'потом'}


def get_html(url):  # возвращает данные сайты в виде тектса
    r = requests.get(url)
    r.encoding = 'utf8'
    return r.text


def get_head(html):
    soup = BeautifulSoup(html, 'lxml')
    return soup


link_mephi = 'https://tabiturient.ru/vuzu/mifi/'
link_mgu = 'https://tabiturient.ru/vuzu/mgu/'
bot = telebot.TeleBot('1449367202:AAEwKojyXQ_hgkPwUKLSWgnqdkuNtJj4zRE')


@bot.message_handler(content_types=['text'])
def get_text_messages(message):  # постоянно принимает сообщения
    if message.text == "/start":
        bot.send_message(message.from_user.id, "Привет, о каком ВУЗе вы хотите получить отзыв?")
        bot.send_message(message.from_user.id, text='Выбор ВУЗа', reply_markup=keyboard)
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /start.")


keyboard = types.InlineKeyboardMarkup()  # создание клавиатуры
key_mephi = types.InlineKeyboardButton(text='МИФИ', callback_data='MEPHI')
key_mgu = types.InlineKeyboardButton(text='МГУ', callback_data='MGU')
keyboard.add(key_mephi)  # Добавление кнопки в клавиатуру
keyboard.add(key_mgu)

keyboard3 = types.InlineKeyboardMarkup()
key_theme = types.InlineKeyboardButton(text='Выбор темы', callback_data='themebtn')
key_eneral = types.InlineKeyboardButton(text='Общий', callback_data='generalbtn')
keyboard3.add(key_theme)
keyboard3.add(key_eneral)

keyboard4 = types.InlineKeyboardMarkup()
key_ob = types.InlineKeyboardButton(text='Общежитие', callback_data='obsh')
key_food = types.InlineKeyboardButton(text='Еда', callback_data='food')
key_teachers = types.InlineKeyboardButton(text='Преподователи', callback_data='teachers')
key_homework = types.InlineKeyboardButton(text='Домашняя работа', callback_data='homework')
key_extra = types.InlineKeyboardButton(text='Дополнительные занятия', callback_data='extra')
keyboard4.add(key_ob)
keyboard4.add(key_food)
keyboard4.add(key_homework)
keyboard4.add(key_teachers)
keyboard4.add(key_extra)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):  # отвечает за кнопки и ответы на сообщения
    global heads
    if call.data == "MEPHI":  # инициализация нажатой кнопки
        link = link_mephi  # ссылка на ВУЗ
        site_name = get_html(link)
        site_data = get_head(site_name)
        head = site_data.find_all('div', class_='font2')  # поиск всех блоков с нужными параметрами
        heads = []
        for e in head:
            heads.append(e.text)  # обработка до приличного состояния
        heads = [e for e in heads if e is not None]
        msg = 'Вы хотите получить общий отзыв ВУЗе или по теме?'
        bot.send_message(call.message.chat.id, msg,
                         reply_markup=keyboard3)  # отсылает сообщение, показывает клавиатуру с выбором

    if call.data == 'MGU':
        link = link_mgu
        site_name = get_html(link)
        site_data = get_head(site_name)
        head = site_data.find_all('div', class_='font2')
        heads = []
        for e in head:
            heads.append(e.text)
        heads = [e for e in heads if e is not None]
        msg = 'Вы хотите получить общий отзыв ВУЗе или по теме?'
        bot.send_message(call.message.chat.id, msg, reply_markup=keyboard3)

    if call.data == 'themebtn':
        msg = 'Выберите тему'
        bot.send_message(call.message.chat.id, msg, reply_markup=keyboard4)

    if call.data == 'generalbtn':  # так как это обычный отзыв, на данном этапе он просто
        # берет некое количество отзывов и делает их краткое содержание.
        # Вскоре эта схема генерации будет заменена на обговоренную
        text = ''
        print(len(heads))
        for i in range(10):  # задаем количество отзывов.
            text += choice(heads)  # На данный момент методом рандома

        sentences = re.split(r' *[\.\?!][\'"\)\]]* *', text)
        clean_text = text.lower()
        word_tokenize = clean_text.split()

        word2count = {}
        for word in word_tokenize:
            if word not in stopwords:
                if word not in word2count.keys():
                    word2count[word] = 1
                else:
                    word2count[word] += 1
        sent2score = {}
        for sentence in sentences:
            for word in sentence.split():
                if word in word2count.keys():
                    if 28 > len(sentence.split(' ')) > 9:
                        if sentence not in sent2score.keys():
                            sent2score[sentence] = word2count[word]
                        else:
                            sent2score[sentence] += word2count[word]

        for key in word2count.keys():
            word2count[key] = word2count[key] / max(word2count.values())

        sentences = heapq.nlargest(7, sent2score, key=sent2score.get)  # вытаскивает семь предложений.
        # Число можно и нужно будет  поменять
        t = ' '.join(sentences)
        bot.send_message(call.message.chat.id, t)  # вывод


bot.polling(none_stop=True, interval=0)
