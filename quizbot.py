import random
import telebot
from telebot import types

TOKEN = '7723306001:AAFuh2Rhbx-Nr63k7m0dnfXS8ImFL8rJF8I'
bot = telebot.TeleBot(TOKEN)

# Create a single instance of QuizBot
quiz_bot = None

class QuizBot:
    def __init__(self):
        self.questions = {
            'etiquette': [
                {
                    'question': '🍽 Какие правила поведения за столом были важны в петровскую эпоху?',
                    'options': [
                        'Чавкать и шуметь за столом',
                        'Не использовать столовые приборы',
                        'Не чавкать и использовать столовые приборы правильно',
                        'Есть руками все блюда'
                    ],
                    'correct': 2,
                    'explanation': '🎯 В петровскую эпоху было важно соблюдать правила этикета за столом, включая правильное использование столовых приборов и отсутствие шума при еде.'
                },
                {
                    'question': '👥 Какие светские манеры были обязательны в обществе?',
                    'options': [
                        'Говорить грубо и дерзко',
                        'Говорить учтиво и держать осанку прямо',
                        'Сутулиться и шептать',
                        'Игнорировать собеседника'
                    ],
                    'correct': 1,
                    'explanation': '🎯 Светские манеры включали вежливую речь и правильную осанку как признаки хорошего воспитания.'
                }
            ],
            'assemblies': [
                {
                    'question': '🎭 Когда были введены ассамблеи Петром I?',
                    'options': [
                        'В 1700 году',
                        'В 1718 году',
                        'В 1725 году',
                        'В 1710 году'
                    ],
                    'correct': 1,
                    'explanation': '🎯 Ассамблеи были введены Петром I в 1718 году как новая форма светской жизни.'
                },
                {
                    'question': '💃 Что было особенного в ассамблеях петровского времени?',
                    'options': [
                        'Только мужчины могли их посещать',
                        'Они были исключительно для иностранцев',
                        'Мужчины и женщины могли свободно общаться',
                        'Они проводились только в церквях'
                    ],
                    'correct': 2,
                    'explanation': '🎯 Впервые на ассамблеях мужчины и женщины могли свободно общаться, что было революционным для того времени.'
                }
            ],
            'clothing': [
                {
                    'question': '👔 Что входило в мужской костюм петровской эпохи?',
                    'options': [
                        'Кафтан, камзол и кюлоты',
                        'Сарафан и кокошник',
                        'Джинсы и футболка',
                        'Тога и сандалии'
                    ],
                    'correct': 0,
                    'explanation': '🎯 Мужской костюм состоял из кафтана (длинного приталенного сюртука), камзола и кюлотов (коротких штанов до колен).'
                },
                {
                    'question': '👗 Какие элементы входили в женский костюм петровской эпохи?',
                    'options': [
                        'Джинсы и блузка',
                        'Сарафан и лапти',
                        'Роброн, корсет и пышная юбка',
                        'Брюки и пиджак'
                    ],
                    'correct': 2,
                    'explanation': '🎯 Женский костюм включал роброн (пышное платье на каркасе), корсет и пышную юбку на каркасе (панье).'
                }
            ],
            'calendar': [
                {
                    'question': '📅 В каком году Петр I издал указ о переходе на новое летоисчисление?',
                    'options': [
                        'В 1700 году',
                        'В 1699 году',
                        'В 1701 году',
                        'В 1695 году'
                    ],
                    'correct': 1,
                    'explanation': '🎯 Указ о переходе на новое летоисчисление был издан в 1699 году.'
                },
                {
                    'question': '📆 Какое изменение произошло в календаре при Петре I?',
                    'options': [
                        'Год стал начинаться 1 марта',
                        'Год стал начинаться 1 января вместо 1 сентября',
                        'Год стал начинаться 1 декабря',
                        'Календарь остался без изменений'
                    ],
                    'correct': 1,
                    'explanation': '🎯 При Петре I началом года стало 1 января вместо 1 сентября, что соответствовало европейской традиции.'
                }
            ]
        }
        self.current_questions = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    global quiz_bot
    quiz_bot = QuizBot()
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    start_button = types.KeyboardButton('🎯 Начать викторину')
    help_button = types.KeyboardButton('❓ Помощь')
    markup.add(start_button, help_button)
    
    welcome_text = """
🎉 *Добро пожаловать в викторину "Быт петровской эпохи"!*

Проверьте свои знания о повседневной жизни при Петре I (1682-1725).

Темы викторины:
📚 Этикет
🎭 Ассамблеи
👔 Одежда
📅 Календарь

Нажмите "🎯 Начать викторину" чтобы получить вопрос!
"""
    bot.reply_to(message, welcome_text, parse_mode='Markdown', reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == '❓ Помощь')
def help_message(message):
    help_text = """
*Как играть в викторину:*

1️⃣ Нажмите "🎯 Начать викторину"
2️⃣ Прочитайте вопрос
3️⃣ Выберите один из вариантов ответа
4️⃣ Получите объяснение и продолжайте играть!

Удачи! 🍀
"""
    bot.reply_to(message, help_text, parse_mode='Markdown')

@bot.message_handler(func=lambda message: message.text == '🎯 Начать викторину')
def start_quiz(message):
    global quiz_bot
    if not quiz_bot:
        quiz_bot = QuizBot()
    
    categories = list(quiz_bot.questions.keys())
    category = random.choice(categories)
    question = random.choice(quiz_bot.questions[category])
    quiz_bot.current_questions[message.from_user.id] = question
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    for i, option in enumerate(question['options']):
        button = types.InlineKeyboardButton(
            text=f"{['A', 'B', 'C', 'D'][i]}. {option}", 
            callback_data=f"answer_{i}"
        )
        markup.add(button)
    
    bot.send_message(
        message.chat.id,
        f"*{question['question']}*",
        parse_mode='Markdown',
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith('answer_'))
def handle_answer(call):
    global quiz_bot
    if not quiz_bot:
        quiz_bot = QuizBot()
        
    try:
        user_id = call.from_user.id
        answer_index = int(call.data.split('_')[1])
        current_question = quiz_bot.current_questions.get(user_id)
        
        if current_question:
            is_correct = answer_index == current_question['correct']
            if is_correct:
                response = "✨ *Правильно!* 🎉\n\n"
            else:
                correct_answer = current_question['options'][current_question['correct']]
                response = f"❌ *Неправильно*\nПравильный ответ: {correct_answer}\n\n"
            
            response += current_question['explanation']
            response += "\n\n🔄 Нажмите '🎯 Начать викторину' для следующего вопроса!"
            
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=response,
                parse_mode='Markdown'
            )
            
            # Answer the callback query to remove the "loading" state
            bot.answer_callback_query(call.id)
    except Exception as e:
        print(f"Error handling answer: {e}")
        bot.answer_callback_query(call.id, text="Произошла ошибка. Попробуйте начать викторину заново.")

if __name__ == "__main__":
    quiz_bot = QuizBot()
    bot.infinity_polling() 