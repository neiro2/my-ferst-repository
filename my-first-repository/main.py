import telebot
import datetime
import time
import threading
import random

bot = telebot.TeleBot('7824180764:AAHeupfy84KqZfVUTryeJb8KD5fWvg1GqCA')

@bot.message_handler(commands = ['start', 'Start', 'старт', 'Старт'])

def start_message(message):
    bot.reply_to(message, "Привет! Я здесь, чтобы помочь тебе заботиться о себе. Я напомню тебе выпить витамины и воду в нужное время. ")
    reminder_thread = threading.Thread(target=send_reminders, args=(message.chat.id,))
    reminder_thread.start()

@bot.message_handler(commands=['help', 'помощь'])
def help_message(message):
        help_text = (
            "Вот список доступных команд:\n"
            "/start - Начать использование бота и получить приветственное сообщение.\n"
            "/factvitamins - Получить случайный факт о витаминах.\n"
            "/factwater - Получить случайный факт о воде.\n"
            "/setreminder - Установить напоминание о приёме витаминов. Введите время и название витамина в формате 'ЧЧ:ММ, витамин'.\n"
            "/help - Показать это сообщение с подсказкой по командам."
        )
        bot.reply_to(message, help_text)


@bot.message_handler(commands=['factvitamins'])
def fact_message(message):
    factvit = ["Витамины были открыты благодаря наблюдению, что морские свинки, питавшиеся очищенным рисом, заболевали серьёзным заболеванием, которое называлось «бери-бери». Позже учёные обнаружили, что добавление в рацион этих животных свежих овощей и фруктов помогало им выздороветь.", "В Средние века люди верили, что определённые продукты, такие как цитрусовые и квашеная капуста, могут вызывать или излечивать цингу — серьёзное заболевание, связанное с дефицитом витамина C.", "Витамин D не только поступает в организм с пищей, но и синтезируется в коже под воздействием солнечного света. Поэтому солнечные ванны могут быть одним из способов получения этого витамина.", "Некоторые животные, такие как морские свинки и крысы, могут синтезировать собственный витамин C, в то время как человеческий организм не способен производить его самостоятельно.", "В Древнем Египте печень считалась ценным продуктом из-за высокого содержания витаминов и минералов."]
    random_fact = random.choice(factvit)
    bot.reply_to(message, f'Лови факт о витаминах: {random_fact}')

@bot.message_handler(commands=['factwater'])
def fact_message(message):
    factwater =  ["Вода на Земле может быть старше самой Солнечной системы: Исследования показывают, что от 30% до 50% воды в наших океанах возможно присутствовала в межзвездном пространстве еще до формирования Солнечной системы около 4,6 миллиарда лет назад.",
"Горячая вода замерзает быстрее холодной: Это явление известно как эффект Мпемба. Под определенными условиями горячая вода может замерзать быстрее, чем холодная, хотя ученые до сих пор полностью не разгадали механизм этого процесса.",
"Больше воды в атмосфере, чем во всех реках мира: Объем водяного пара в атмосфере Земли в любой момент времени превышает объем воды во всех реках мира вместе взятых. Это подчеркивает важную роль атмосферы в гидрологическом цикле, перераспределяя воду по планете."]

    random_fact = random.choice(factwater)
    bot.reply_to(message, f'Лови факт о воде {random_fact}')


user_reminders = {}  # Словарь для хранения напоминаний пользователей


@bot.message_handler(commands=['setreminder'])
def set_reminder(message):
    msg = bot.reply_to(message,
                       "Введите время для вашего напоминания в формате ЧЧ:ММ и название витамина  (например, 14:30 витамин C).")
    bot.register_next_step_handler(msg, save_reminder)


def save_reminder(message):
    try:
        chat_id = message.chat.id
        data = message.text.strip().split(',')

        if len(data) != 2:
            raise ValueError("Неверный формат ввода")

        reminder_time, vitamin = data[0].strip(), data[1].strip()
        datetime.datetime.strptime(reminder_time, "%H:%M")  # Проверка формата времени

        user_reminders[chat_id] = (reminder_time, vitamin)
        bot.reply_to(message, f"Напоминание установлено на {reminder_time} для {vitamin}!")
    except ValueError:
        bot.reply_to(message, "Неправильный формат. Пожалуйста, используйте формат ЧЧ:ММ, витамин.")


def send_reminders():
    while True:
        now = datetime.datetime.now().strftime("%H:%M")
        for chat_id, (reminder_time, vitamin) in user_reminders.items():
            if now == reminder_time:
                bot.send_message(chat_id, f"Время для вашего напоминания - выпейте воды и примите {vitamin}!")
                time.sleep(61)  # Избегайте отправки нескольких сообщений одновременно
        time.sleep(1)

def main():
    reminder_thread = threading.Thread(target=send_reminders,)
    reminder_thread.start()


if __name__ == "__main__":
    main()


bot.polling(non_stop=True)