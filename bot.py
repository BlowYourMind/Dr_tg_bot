import telebot
import config
import random
from datetime import datetime

from HdRezkaApi import *

bot = telebot.TeleBot(config.TOKEN)

phrases = [
    "{0.first_name} очень красивая",
    "{0.first_name} очень умная",
    "{0.first_name} веселая",
    "{0.first_name} загадочная",
    "{0.first_name} бесстрашная",
    "{0.first_name} иногда ленивая)",
    "{0.first_name} очень крутая",
]

imgs = [
    open("./static/sticker.webp", "rb"),
    open("./static/sticker1.webp", "rb"),
    open("./static/sticker2.webp", "rb"),
    open("./static/sticker3.webp", "rb"),
    open("./static/sticker4.webp", "rb"),
]


# Function to calculate time remaining until a specific date and time
def time_until(target_date):
    now = datetime.now()
    target = datetime.strptime(target_date, "%d.%m.%Y %H:%M")
    delta = target - now
    return delta


def correct_phrase_for_hours(hours):
    if hours == 1 or hours == 21:
        return "час"

    elif 2 <= hours <= 4 or 22 <= hours <= 24:
        return "часа"
    else:
        return "часов"


def correct_phrase_for_minutes(minutes):
    if minutes == 1 or minutes == 21 or minutes == 31 or minutes == 41 or minutes == 51:
        return "минута"
    elif (
        2 <= minutes <= 4
        or 22 <= minutes <= 24
        or 32 <= minutes <= 34
        or 42 <= minutes <= 44
        or 52 <= minutes <= 54
    ):
        return "минуты"
    else:
        return "минут"


def correct_phrase_for_seconds(seconds):
    if seconds == 1 or seconds == 21 or seconds == 31 or seconds == 41 or seconds == 51:
        return "секунда"
    elif (
        2 <= seconds <= 4
        or 22 <= seconds <= 24
        or 32 <= seconds <= 34
        or 42 <= seconds <= 44
        or 52 <= seconds <= 54
    ):
        return "секунды"
    else:
        return "секунд"


@bot.message_handler(commands=["start"])
def welcome(message):
    bot.send_message(
        message.chat.id,
        "Привет {0.first_name}, я был создан для тебя. Моей главной задачей будет показывать, сколько осталось времени до твоего дня рождения)".format(
            message.from_user, bot.get_me()
        ),
        parse_mode="html",
    )


@bot.message_handler(content_types=["text"])
def lalala(message):
    print(message)
    print(message.from_user.first_name, message.text)
    # bot.send_sticker(message.chat.id, random.choice(imgs))

    # Calculate time remaining until April 2, 2024, at 11:30
    remaining_time = time_until("02.04.2024 11:30")
    days = remaining_time.days
    hours, remainder = divmod(remaining_time.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    bot.send_message(
        message.chat.id,
        f"До твоего дня рождения осталось {days} дней, {hours} {correct_phrase_for_hours(hours)}, {minutes} {correct_phrase_for_hours(minutes)}, {seconds} {correct_phrase_for_seconds(seconds)}",
    )


bot.polling(none_stop=True)
