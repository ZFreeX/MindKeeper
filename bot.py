#!/usr/bin/env python
# -*- coding: utf-8 -*-
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton, ParseMode, CallbackQuery
import asyncio
import sqlite3 as sql
import random
from aiogram.utils.markdown import text, bold, italic, code, pre
from bs4 import BeautifulSoup
import urllib.request
from urllib.parse import quote
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split


bot = Bot(token="5216070611:AAGdv9ZSiAeZ8NstQLlYBvtIZMHQmbocuNc")
dp = Dispatcher(bot)

keys = {"1": "programming", "2": "informatics", "3": "biology", "4": "physics"}


print("we are wok")

coolarts = [1, 3, 9, 10, 69, 137, 152, 172, 177, 181, 391, 411, 425, 426, 438, 452, 460, 467, 489, 493]




async def task():
    con = sql.connect("users.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM `users`")

    #programming books
    url = "https://labirint.ru"
    link = "https://www.labirint.ru/genres/2308/?page="
    link += str(random.randint(1, 17))
    req = urllib.request.urlopen(link)
    req = req.read()

    soup = BeautifulSoup(req, "html.parser")
    items = soup.select("a.cover")
    i = random.randint(0, len(items)-1)
    s = items[i].get("title")
    title1 = s[s.find("-")+2:].replace("'", "")
    h1 = url + items[i].get("href")

    #physics books
    url = "https://aldebaran.ru"
    link = "https://aldebaran.ru/genre/nauka_obrazovanie/fizika/pagenum-"+str(random.randint(1,15))
    link = urllib.request.Request(link, headers={'User-Agent' : "Magic Browser"})
    req = urllib.request.urlopen(link)
    req = req.read()
    soup = BeautifulSoup(req, "html.parser")
    items = soup.select("p.booktitle a")
    i = random.randint(0, len(items) - 1)
    title2 = items[i].get_text().replace("'", "")
    h2 = url + items[i].get("href")

    #biology articles
    url = "https://biomolecula.ru"
    link = url + "/articles?page="+str(random.randint(1, 20))
    req = urllib.request.urlopen(link)
    req = req.read()
    soup = BeautifulSoup(req, "html.parser")
    items = soup.select("a.article-item_title")
    i = random.randint(0, len(items) - 1)
    title3 = items[i].get_text().replace("'", "")
    h3 = url + items[i].get("href")

    #informatics articles
    url = "https://ru.algorithmica.org"
    req = urllib.request.urlopen(url)
    req = req.read()
    soup = BeautifulSoup(req, "html.parser")
    items = soup.select("a")
    i = random.randint(0, len(items) - 1)
    title4 = items[i].get_text().replace("'", "")
    h4 = items[i].get("href")

    rows = cur.fetchall()
    for row in rows:
        if row[2] == 0:
            continue
        fs = [] #список
        sent = False
        cur.execute(f"SELECT * FROM `{row[0]}`")
        curs = cur.fetchall()
        headers = [x[0] for x in curs]
        y = [x[1] for x in curs]
        if len(headers) == 0 or len(y) == 0:
            continue
        vectorizer = TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 3))
        X = vectorizer.fit_transform(headers)
        clf = SVC(probability=True)
        clf.fit(X, y)
        print("Исследовать: ", title1, sep=" ")
        zz = clf.predict_proba(vectorizer.transform([title1]))
        f = zz[0][0]
        ff = round(f, 2)
        fff = ff * 100
        z = clf.predict(vectorizer.transform([title1]))
        print(z)
        print("result: ", fff, "%", sep=" ")
        #####valid test
        # scores = []
        # for i in range(10):
        #     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33)
        #
        #     clf2 = LogisticRegression(random_state=0)
        #     clf2.fit(X_train, y_train)
        #     score = clf2.score(X_test, y_test)
        #     scores.append(score)
        # t = sum(scores)/len(scores)
        # tt = round(t, 2)
        # print("VALID FOR ", 100*tt, sep=" ")
        ####
        fs.append((fff, title1, h1, "programming"))
        if z == "Даz":
            t = "🔮 <b>" + title1 + "</b>\n\n"
            t += "📍 Область: <i>"
            t += "" \
                 "programming</i>"
            t += "\n🔎 Ссылка: " + h1
            if t[len(t) - 1] != '/':
                t += '/'
            kb = InlineKeyboardMarkup()
            kb.add(InlineKeyboardButton("Интересно 🟢", callback_data="yes"))
            kb.add(InlineKeyboardButton("Неинтересно 🔴", callback_data="no"))
            await bot.send_message(row[0], t, reply_markup=kb, parse_mode=ParseMode.HTML)
            sent = True

        print("Исследовать: ", title2, sep=" ")
        zz = clf.predict_proba(vectorizer.transform([title2]))
        f = zz[0][0]
        ff = round(f, 2)
        fff = ff * 100
        z = clf.predict(vectorizer.transform([title2]))
        print(z)
        print("result: ", fff, "%", sep=" ")
        fs.append((fff, title2, h2, "physics"))

        # #####valid test
        # scores = []
        # for i in range(10):
        #     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33)
        #
        #     clf2 = LogisticRegression(random_state=0)
        #     clf2.fit(X_train, y_train)
        #     score = clf2.score(X_test, y_test)
        #     scores.append(score)
        # t = sum(scores) / len(scores)
        # tt = round(t, 2)
        # print("VALID FOR ", 100 * tt, sep=" ")
        ####

        if z == "Даz":
            t = "🔮 <b>" + title2 + "</b>\n\n"
            t += "📍 Область: <i>"
            t += "" \
                 "physics</i>"
            t += "\n🔎 Ссылка: " + h2
            if t[len(t) - 1] != '/':
                t += '/'
            kb = InlineKeyboardMarkup()
            kb.add(InlineKeyboardButton("Интересно 🟢", callback_data="yes"))
            kb.add(InlineKeyboardButton("Неинтересно 🔴", callback_data="no"))
            await bot.send_message(row[0], t, reply_markup=kb, parse_mode=ParseMode.HTML)
            sent = True

        print("Исследовать: ", title3, sep=" ")
        zz = clf.predict_proba(vectorizer.transform([title3]))
        f = zz[0][0]
        ff = round(f, 2)
        fff = ff * 100
        z = clf.predict(vectorizer.transform([title3]))
        print(z)
        print("result: ", fff, "%", sep=" ")
        fs.append((fff, title3, h3, "biology"))
        # #####valid test
        # scores = []
        # for i in range(10):
        #     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33)
        #
        #     clf2 = LogisticRegression(random_state=0)
        #     clf2.fit(X_train, y_train)
        #     score = clf2.score(X_test, y_test)
        #     scores.append(score)
        # t = sum(scores) / len(scores)
        # tt = round(t, 2)
        # print("VALID FOR ", 100 * tt, sep=" ")
        ####
        if z == "Даz":
            t = "🔮 <b>" + title3 + "</b>\n\n"
            t += "📍 Область: <i>"
            t += "" \
                 "biology</i>"
            t += "\n🔎 Ссылка: " + h3
            if t[len(t) - 1] != '/':
                t += '/'
            kb = InlineKeyboardMarkup()
            kb.add(InlineKeyboardButton("Интересно 🟢", callback_data="yes"))
            kb.add(InlineKeyboardButton("Неинтересно 🔴", callback_data="no"))
            await bot.send_message(row[0], t, reply_markup=kb, parse_mode=ParseMode.HTML)
            sent = True

        print("Исследовать: ", title4, sep=" ")
        zz = clf.predict_proba(vectorizer.transform([title4]))
        f = zz[0][0]
        ff = round(f, 2)
        fff = ff * 100
        z = clf.predict(vectorizer.transform([title4]))
        print(z)
        print("result: ", fff, "%", sep=" ")
        fs.append((fff, title4, h4, "informatics"))
        #####valid test
        scores = []
        # for i in range(10):
        #     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33)
        #
        #     clf2 = LogisticRegression(random_state=0)
        #     clf2.fit(X_train, y_train)
        #     score = clf2.score(X_test, y_test)
        #     scores.append(score)
        # t = sum(scores) / len(scores)
        # tt = round(t, 2)
        # print("VALID FOR ", 100 * tt, sep=" ")
        ####
        if z == "Даz" and h4 != None:
            t = "🔮 <b>" + title4 + "</b>\n\n"
            t += "📍 Область: <i>"
            t += "" \
                 "informatics</i>"
            t += "\n🔎 Ссылка: " + h4
            if t[len(t) - 1] != '/':
                t += '/'
            kb = InlineKeyboardMarkup()
            kb.add(InlineKeyboardButton("Интересно 🟢", callback_data="yes"))
            kb.add(InlineKeyboardButton("Неинтересно 🔴", callback_data="no"))
            await bot.send_message(row[0], t, reply_markup=kb, parse_mode=ParseMode.HTML)
            sent = True
        if sent == False:
            print("emergency comparing...")
            fs.sort(key=lambda x: -x[0])
            t = "🔮 <b>" + fs[0][1] + "</b>\n\n"
            t += "📍 Область: <i>"
            t += "" \
                 f"{fs[0][3]}</i>"
            t += "\n🔎 Ссылка: " + fs[0][2]
            if t[len(t) - 1] != '/':
                t += '/'
            kb = InlineKeyboardMarkup()
            kb.add(InlineKeyboardButton("Интересно 🟢", callback_data="yes"))
            kb.add(InlineKeyboardButton("Неинтересно 🔴", callback_data="no"))
            await bot.send_message(row[0], t, reply_markup=kb, parse_mode=ParseMode.HTML)
            t = "🔮 <b>" + fs[1][1] + "</b>\n\n"
            t += "📍 Область: <i>"
            t += "" \
                 f"{fs[1][3]}</i>"
            t += "\n🔎 Ссылка: " + fs[1][2]
            if t[len(t) - 1] != '/':
                t += '/'
            await bot.send_message(row[0], t, reply_markup=kb, parse_mode=ParseMode.HTML)







@dp.message_handler(commands=['start'])
async def process(msg: types.Message):
    mk = ReplyKeyboardMarkup(resize_keyboard=True)
    mk.add(KeyboardButton("Мои интересы 🔥"), KeyboardButton("Настройки ⚙️"))
    mk.add("Очистить 🧨")
    await bot.send_message(msg.from_user.id, "Главное меню 👇\nДля того, чтобы начать получать рассылку, тебе нужно оценить первичный набор материалов. Кликай на кнопку 'Мои интересы 🔥'\n\n⛓ После оценки первых статей и книг включи рассылку в настройках!\n\n⚠️ Кнопка очистки удаляет все оценки пользователя из базы данных, нейронную сеть нужно будет обучать заново по кнопке 'Мои интересы 🔥'\n\n Обязательно ознакомься с командой /help!", reply_markup=mk)
    con = sql.connect("users.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS `users`(`id` INTEGER, `interests` STRING, `mode` INTEGER)")
    cur.execute("SELECT * FROM `users`")
    rows = cur.fetchall()
    y = False
    for row in rows:
        if row[0] == msg.from_user.id:
            y = True

    if y == False:
        cur.execute(f"INSERT INTO `users` values('{msg.from_user.id}', 'default', '0')")

    con.commit()
    cur.close()


@dp.message_handler(commands=['help'])
async def help(msg: types.Message):
    await bot.send_message(msg.from_user.id, "📮 Бот позволяет получать <b>книги</b> и <b>статьи</b> на основе <b>анализа твоих интересов</b>, построенном на обработке заголовков.\n\n📊 На текущий момент пользователи получают материалы из следующих областей:\n<i>• Программирование и разработка\n• Биология\n• Физика\n• Информатика и алгоритмы</i>\n\nСписок охватываемых областей будет расширяться.\n\nСтарт работы с ботом:\n1. Нажать кнопку 'Мои интересы 🔥'\n2. Получить 20 статей/книг\n3. Разделить материалы на интересные и неинтересные.\n4. Успешное выполнение <b>пункта 3</b> создаст почву для первичного обучения нейронной сети, и бот начнет присылать статьи и книги.\n5. Оценка каждой свежеполученной статьи/книги делает рекомендации системы более точными, не пренебрегай этим :)\n\n🛡 Особенности работы системы:\nПо задумке рассылка происходит каждые <b>12 часов</b>, но на момент тестов перерыв снижен до <b>10 минут</b>. Иногда система будет рекомендовать тебе то, что будет новым для тебя и редко встречалось до этого среди твоих интересов для расширения твоего кругозора :)\n\n⚙️ Отключить/включить рассылку можно в настройках.\n\n 👤 Author: @ZFreeX"
                                             "", parse_mode=ParseMode.HTML)




@dp.callback_query_handler(lambda c: c.data == "delete")
async def proccess(callback_query: CallbackQuery):
    con = sql.connect("users.db")
    cur = con.cursor()
    cur.execute(f"DELETE FROM `{callback_query.from_user.id}`")
    await callback_query.message.edit_text("Очистка завершена 🌀")
    cur.execute(f"UPDATE `users` SET interests = 'default' WHERE id ={callback_query.from_user.id}")
    con.commit()
    cur.close()


@dp.callback_query_handler(lambda c: c.data == 'yes')
async def process_callback_button1(callback_query: CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.edit_text("💥 Оценено!\n"+callback_query.message.text)
    #подключение к персональной таблице
    s = callback_query.message.text
    caption = s[2:s.find("\n")]
    con = sql.connect("users.db")
    cur = con.cursor()
    cur.execute(f"INSERT INTO `{callback_query.from_user.id}` values('{caption}', 'Да')")
    con.commit()
    cur.close()


@dp.callback_query_handler(lambda c: c.data == 'no')
async def process_callback_button1(callback_query: CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.edit_text("💥 Оценено!\n"+callback_query.message.text)
    s = callback_query.message.text
    caption = s[2:s.find("\n")]
    con = sql.connect("users.db")
    cur = con.cursor()
    cur.execute(f"INSERT INTO `{callback_query.from_user.id}` values('{caption}', 'Нет')")
    con.commit()
    cur.close()


@dp.message_handler(commands=['id'])
async def m(msg: types.Message):
    await bot.send_message(msg.from_user.id, msg.from_user.id)

@dp.message_handler(commands=['task'])
async def m(msg: types.Message):
    await task()
    await bot.send_message(msg.from_user.id, "completed. ")


@dp.message_handler(commands=['change'])
async def proc(msg: types.Message):
    con = sql.connect("users.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM `users`")
    rows = cur.fetchall()

    for row in rows:
        if row[0] == msg.from_user.id:
            mode = row[2]

    if mode == 0:
        mode = 1
    else:
        mode = 0
    cur.execute(f"UPDATE `users` SET mode = {mode} WHERE id = {msg.from_user.id}")
    await bot.send_message(msg.from_user.id, "Режим изменен. ")
    con.commit()
    cur.close()


#последний обработчик

@dp.message_handler()
async def process(msg: types.Message):
    if msg.text == "Настройки ⚙️":
        con = sql.connect("users.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM `users`")
        rows = cur.fetchall()

        for row in rows:
            if row[0] == msg.from_user.id:
                mode = row[2]

        #bt1 = InlineKeyboardButton("Поменять режим 🧬", callback_data="change_{}".format(msg.from_used.id))
        #kb = InlineKeyboardMarkup().add(bt1)
        if mode == 0:
            s = italic("рассылка отключена ❌")
        else:
            s = italic("рассылка включена ✅")
        await bot.send_message(msg.from_user.id, "🔑 Твой режим: {}\n/change - команда для его изменения. ".format(s), parse_mode=ParseMode.MARKDOWN)
        cur.close()
    elif msg.text == "Очистить 🧨":
        kb = InlineKeyboardMarkup()
        kb.add(InlineKeyboardButton("Удалить все данные 🚫", callback_data="delete"))
        await bot.send_message(msg.from_user.id, "Это действие полностью очистит все ваши интересы, известные боту. Продолжить?", reply_markup=kb)
    elif msg.text == "Мои интересы 🔥":
        con = sql.connect("users.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM `users`")
        rows = cur.fetchall()

        for row in rows:
            if row[0] == msg.from_user.id:
                s = row[1]


        if s == "default":
            await bot.send_message(msg.from_user.id, "Для того, чтобы бот знал твои предпочтения, ты получишь 20 статей/книг, которые должен будешь разделить на две группы - интересные и неинтересные. ")
            ind = 0
            con2 = sql.connect("new_articles.db")
            cur2 = con2.cursor()
            cur2.execute("SELECT * FROM `articles`")
            cur.execute(f"CREATE TABLE IF NOT EXISTS `{msg.from_user.id}`('title' STRING, 'intent' STRING)")
            rows = cur2.fetchall()
            k = 0
            for row in rows:
                k += 1
                if ind >= len(coolarts):
                    break
                if k == coolarts[ind]:
                    ind += 1

                    t = "🔮 <b>"+row[0] + "</b>\n\n"
                    t += "📍 Область: <i>"
                    t += italic(row[3])+"</i>"
                    t += "\n🔎 Ссылка: " + row[2]
                    if t[len(t)-1] != '/':
                        t += '/'
                    kb = InlineKeyboardMarkup()
                    kb.add(InlineKeyboardButton("Интересно 🟢", callback_data="yes"))
                    kb.add(InlineKeyboardButton("Неинтересно 🔴", callback_data="no"))
                    await bot.send_message(msg.from_user.id, t, reply_markup=kb, parse_mode=ParseMode.HTML)
            con2.commit()
            cur2.close()

            cur.execute(f"UPDATE `users` SET interests = 'accepted' WHERE id = {msg.from_user.id}")
        else:
            await bot.send_message(msg.from_user.id, "👋 Твои предпочтения уже занесены в базу данных. Жди следующей рассылки :)")


        con.commit()
        cur.close()


#DELAY = 12*3600
DELAY = 10


def repeat(coro, loop):
    asyncio.ensure_future(coro(), loop=loop)
    loop.call_later(DELAY, repeat, coro, loop)

async def func():
    await task()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.call_later(DELAY, repeat, func, loop)
    executor.start_polling(dp)

