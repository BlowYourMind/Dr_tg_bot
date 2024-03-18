import telebot
import config
from datetime import datetime, timedelta
import threading
import time  # Add this line to import the time module

bot = telebot.TeleBot(config.TOKEN)

# Global variable to store total time remaining
total_time_remaining = 0
chat_id = None  # Global variable to store the chat_id

def initialize_time_remaining():
    global total_time_remaining
    # Calculate time remaining until the specified date and time
    target_date = "19.03.2024 01:07"
    total_time_remaining = time_until(target_date).total_seconds()

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
    global chat_id
    chat_id = message.chat.id  # Store the chat_id
    bot.send_message(
        message.chat.id,
        "Привет {0.first_name}, я был создан для тебя. Моей главной задачей будет показывать, сколько осталось времени до твоего дня рождения)".format(
            message.from_user, bot.get_me()
        ),
        parse_mode="html",
    )
    initialize_time_remaining()  # Initialize time remaining when the bot starts
    send_countdown_messages()

@bot.message_handler(content_types=["text"])
def lalala(message):
    global total_time_remaining
    print(message.from_user.first_name, message.text)

    days, remainder = divmod(total_time_remaining, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)

    bot.send_message(
        message.chat.id,
        f"До твоего дня рождения осталось {int(days)} дней, {int(hours)} {correct_phrase_for_hours(hours)}, {int(minutes)} {correct_phrase_for_minutes(minutes)}, {int(seconds)} {correct_phrase_for_seconds(seconds)}",
    )

    # Start a separate thread to continuously send messages while waiting
    # threading.Thread(target=send_countdown_messages, args=(message.chat.id,)).start()

def send_countdown_messages():
    global total_time_remaining, chat_id
    while total_time_remaining > 0:
        time.sleep(1)
        total_time_remaining -= 1
        print(total_time_remaining)
        if 0 < total_time_remaining < 1:
            bot.send_message(
                chat_id,
                f"s днem рождения!"
            )

# Start the bot
bot.polling(none_stop=True)
