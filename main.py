import telebot

TOKEN = 'YOUR-TOKEN'

bot = telebot.TeleBot(TOKEN)

readyIds = []
searchingGames = set()
games = {}
pickedASubject = {}
waitingResult = []


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    msg = message.text
    global searchingGames
    print(message.from_user.id, "написал", msg)
    if msg.lower() == "да" and message.from_user.id in readyIds:
        bot.send_message(message.from_user.id, 'Хорошо, ожидайте.')

        searchingGames.add(message.from_user.id)
        index = readyIds.index(message.from_user.id)
        readyIds.pop(index)

        if len(searchingGames) >= 2:
            searchingGames = list(searchingGames)
            player1, player2 = searchingGames[0], searchingGames[-1]

            bot.send_message(player1, 'Игра нашлась. Напишите "камень", "ножницы" или "бумага".')
            bot.send_message(player2, 'Игра нашлась. Напишите "камень", "ножницы" или "бумага".')

            games[player1] = player2
            games[player2] = player1

            pickedASubject[player1] = ""
            pickedASubject[player2] = ""

            searchingGames = searchingGames[1:-1]
            searchingGames = set(searchingGames)

    elif msg.lower() == "нет" and message.from_user.id in readyIds:
        bot.send_message(message.from_user.id, 'Жалко. Возвращайтесь скорее!')

        index = readyIds.index(message.from_user.id)
        readyIds.pop(index)
    elif (msg.lower() == "камень" or msg.lower() == "бумага" or msg.lower() == "ножницы") and message.from_user.id in games.keys():
        pickedASubject[message.from_user.id] = msg.lower()
        if pickedASubject[games[message.from_user.id]] != "":
            waitingResult.append((message.from_user.id, games[message.from_user.id]))
            print(waitingResult, pickedASubject)
            player1, player2 = waitingResult[0]

            subject1 = pickedASubject[player1]
            subject2 = pickedASubject[player2]

            if subject1 == "бумага":
                if subject2 == "камень":
                    bot.send_message(player1, "Вы выиграли.")
                    bot.send_message(player2, 'Вы проиграли.')
                elif subject2 == "бумага":
                    bot.send_message(player1, "Ничья.")
                    bot.send_message(player2, 'Ничья.')
                else:
                    bot.send_message(player2, "Вы выиграли.")
                    bot.send_message(player1, 'Вы проиграли.')
            elif subject1 == "камень":
                if subject2 == "камень":
                    bot.send_message(player1, "Ничья.")
                    bot.send_message(player2, 'Ничья.')
                elif subject2 == "бумага":
                    bot.send_message(player2, "Вы выиграли.")
                    bot.send_message(player1, 'Вы проиграли.')
                else:
                    bot.send_message(player1, "Вы выиграли.")
                    bot.send_message(player2, 'Вы проиграли.')
            else:
                if subject2 == "камень":
                    bot.send_message(player2, "Вы выиграли.")
                    bot.send_message(player1, 'Вы проиграли.')
                elif subject2 == "бумага":
                    bot.send_message(player1, "Вы выиграли.")
                    bot.send_message(player2, 'Вы проиграли.')
                else:
                    bot.send_message(player1, "Ничья.")
                    bot.send_message(player2, 'Ничья.')

            bot.send_message(player1, 'Хотите сыграть ещё раз? ("да" или "нет")')
            bot.send_message(player2, 'Хотите сыграть ещё раз? ("да" или "нет")')

            games.pop(player1, None)
            games.pop(player2, None)

            pickedASubject.pop(player1, None)
            pickedASubject.pop(player2, None)

            waitingResult.pop(0)

            readyIds.append(player1)
            readyIds.append(player2)
        else:
            bot.send_message(games[message.from_user.id], "Ваш противник выбрал предмет. Ждём вас.")
    else:
        if message.from_user.id in readyIds:
            bot.send_message(message.from_user.id, 'Ответ некорректный. Напишите "да" или "нет".')
        elif message.from_user.id in games:
            bot.send_message(message.from_user.id, 'Неверный предмет. Попробуйте ещё раз.')
            bot.send_message(message.from_user.id, 'Напишите "камень", "ножницы" или "бумага".')
        elif message.from_user.id in searchingGames:
            bot.send_message(message.from_user.id, "Ждите, игра скоро начнётся.")
        else:
            bot.send_message(message.from_user.id, 'Хочешь сыграть в игру? ("да" или "нет")')
            readyIds.append(message.from_user.id)

bot.infinity_polling()