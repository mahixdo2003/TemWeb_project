import telebot
import base
import web_api


bot = telebot.TeleBot(base.TOKEN)

# def get_books():

#     url = "https://books.toscrape.com/"

#     response = requests.get(url)
#     soup = BeautifulSoup(response.text, "html.parser")
#     return soup.select("article.product_pod")


print("Book Bot Created ...")


# --------------------------------

@bot.message_handler(commands=['start'])
def start(message):

    bot.send_message(
        message.chat.id,
        "سلام! به ربات کتاب خوش اومدی"
    )

    show_menu(message)
#-------------------------------------------

@bot.message_handler(commands=['help'])
def help(message):

    bot.reply_to(
        message,"ایدی پشتیبانی = @mahixdo"
    )


# --------------------------------

@bot.message_handler(commands=['menu'])
def show_menu(message):

    markup = telebot.types.ReplyKeyboardMarkup(
        resize_keyboard=True
    )

    btn1 = telebot.types.KeyboardButton("لیست کتاب ")
    btn2 = telebot.types.KeyboardButton("جستجوی کتاب")

    markup.add(btn1, btn2)

    bot.send_message(
        message.chat.id,
        "یکی از گزینه رو انتخاب کن:",
        reply_markup=markup
    )
#---------------------------------------------------------------
@bot.message_handler(commands=['list'])
def show_books_message(message):

    result = web_api.get_books()

    text = "Book List:\n\n"

    for book in result:
        text += f"Name: {book['name']}\n"
        text += f"Price: {book['price']}\n\n"

    bot.send_message(message.chat.id, text)

# --------------------------------------------------------
@bot.message_handler(commands=['search'])
def search_book(message):

    msg = bot.send_message(
        message.chat.id,
        "اسم کتاب رو وارد کن:"
    )

    bot.register_next_step_handler(msg, search_result)


def search_result(message):

    name = message.text.lower()

    result = web_api.get_books()

    found = False

    for book in result:

        if name in book['name'].lower():

            text = f"Name: {book['name']}\n"
            text += f"Price: {book['price']}"

            bot.send_message(message.chat.id, text)

            found = True

    if not found:

        bot.send_message(
            message.chat.id,
            "Book not found!"
        )


#-----------------------------------------------------
if __name__ == '__main__':
    bot.infinity_polling()