import logging
from datetime import datetime
import requests
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, \
    InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, ConversationHandler, CallbackContext, Filters, \
    CallbackQueryHandler
import psycopg2
from config.settings import env

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

conn = psycopg2.connect(dbname=env('NAME'), user=env("USER"), password=env('PASSWORD'), host=env("HOST"))
cursor = conn.cursor()

PHONE, NAME, MAIN_MENU, ORDER, QUANTITY, LOCATION, CONFIRM, SUPPORT = range(8)


def get_adress(lat, long):
    response = requests.get(
        f'https://geocode.maps.co/reverse?lat={lat}&lon={long}&api_key=668e511aec72a355132956hlnc0a7b4')
    data = response.json()
    adres = data['display_name']
    return adres


def start(update: Update, context: CallbackContext) -> int:
    user_id = update.message.from_user.id
    cursor.execute("SELECT * FROM users WHERE telegram_id = %s", (user_id,))
    user = cursor.fetchone()
    if user:
        return main_menu(update, context)
    else:
        reply_keyboard = [[KeyboardButton("Telefon raqamni yuborish", request_contact=True)]]
        update.message.reply_text(
            'Assalomu alaykum, iltimos telefon raqamingizni yuboring',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
        )
        return PHONE


def phone_number(update: Update, context: CallbackContext) -> int:
    user_id = update.message.from_user.id
    phone = update.message.contact.phone_number
    context.user_data['phone'] = phone

    update.message.reply_text(
        "Ismingizni kiriting",
        reply_markup=ReplyKeyboardRemove()
    )
    return NAME


def name(update: Update, context: CallbackContext) -> int:
    user_id = update.message.from_user.id
    full_name = update.message.text

    context.user_data['full_name'] = full_name
    cursor.execute("INSERT INTO users (telegram_id, phone, full_name, is_active, is_staff, is_superuser, date_joined, email, lang, password) "
                   "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                   (user_id, context.user_data['phone'], full_name, True, False, False, datetime.now(), f'{full_name.lower()}@mail.com', 'uz', f'{full_name.lower()}'))
    conn.commit()

    return main_menu(update, context)


def main_menu(update: Update, context: CallbackContext) -> int:
    reply_keyboards = [['Buyurtma berish', "Mening buyurtmalarim"], ["Qo'lab quvvatlash"]]
    update.message.reply_text(
        "Asosiy menu:",
        reply_markup=ReplyKeyboardMarkup(reply_keyboards, one_time_keyboard=True, resize_keyboard=True)
    )
    return MAIN_MENU


def order_water(update: Update, context: CallbackContext) -> int:
    cursor.execute("SELECT name FROM products;")
    products = cursor.fetchall()
    product_names = []
    for product in list(products):
        i = 0
        product = product[i]
        product_names.append(product)
        i += 1
        if i > len(products):
            break
    context.user_data['product_names'] = product_names

    reply_keyboard = [product_names]
    update.message.reply_text(
        "Necha litr suv olasiz?",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
    )
    return ORDER


def set_order(update: Update, context: CallbackContext) -> int:
    context.user_data['item'] = update.message.text
    update.message.reply_text(
        "Nechta suv olasiz?",
        reply_markup=ReplyKeyboardRemove()
    )
    return QUANTITY


def set_quantity(update: Update, context: CallbackContext) -> int:
    context.user_data['quantity'] = int(update.message.text)
    update.message.reply_text(
        'Locaksiyangizni yuboring',
        reply_markup=ReplyKeyboardRemove()
    )
    return LOCATION


def set_location(update: Update, context: CallbackContext) -> int:
    location = update.message.location

    context.user_data['latitude'] = location.latitude
    context.user_data['longitude'] = location.longitude
    location = get_adress(context.user_data['latitude'], context.user_data['longitude'])
    item = context.user_data['item']
    quantity = context.user_data['quantity']
    cursor.execute("SELECT price FROM products")
    products_price = cursor.fetchall()
    products_prices = []
    for product_price in list(products_price):
        i = 0
        product_price = product_price[i]
        products_prices.append(product_price)
        i += 1
    products_name = context.user_data['product_names']

    prices = {}
    for i in range(len(products_name)):
        prices[products_name[i]] = products_prices[i]

    per_item_price = prices[item]
    context.user_data['per_item_price'] = per_item_price
    total_price = per_item_price * quantity

    context.user_data['total_price'] = total_price

    order_detail = (f"Suv tafsilotlari:\n"
                    f"Suv: {item}\n"
                    f"Soni: {quantity}\n"
                    f"Locatsiya: {location}\n"
                    f"Jami narx: ${total_price:.2f}\n"
                    )
    reply_keyboard = [['Tasdiqlash', 'Bekor qilish']]
    update.message.reply_text(
        order_detail,
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
    )
    return CONFIRM


def confirm_order(update: Update, context: CallbackContext) -> int:
    if update.message.text.lower() == 'tasdiqlash':
        user_id = update.message.from_user.id
        item = context.user_data['item']
        quantity = context.user_data['quantity']
        longitude = context.user_data['longitude']
        latitude = context.user_data['latitude']
        total_price = context.user_data['total_price']
        status = 'Created'
        location = get_adress(latitude, longitude)
        print(location)
        cursor.execute('INSERT INTO orders (customer_id, product_id, count, location, total_price, status, free_count, longitude, latitude, status_changed_at, product_price, created_at, updated_at) VALUES '
                       "((SELECT id FROM users WHERE telegram_id = %s), (SELECT id FROM products WHERE name = %s), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                        (user_id, item, quantity, location, total_price, status, 1, longitude, latitude, datetime.now(), context.user_data['per_item_price'], datetime.now(), datetime.now()))
        conn.commit()

        update.message.reply_text(
            "Buyurtma qabul qilindi",
            reply_markup=ReplyKeyboardRemove()
        )
    else:
        update.message.reply_text(
            "Buyurtma yaratish bekor qilindi",
            reply_markup=ReplyKeyboardRemove()
        )
    return main_menu(update, context)


def my_orders(update: Update, context: CallbackContext) -> int:
    user_id = update.message.from_user.id
    cursor.execute("SELECT id FROM users WHERE telegram_id = %s", (user_id,))
    user = cursor.fetchone()

    if user:
        cursor.execute("SELECT * FROM orders WHERE customer_id = %s ORDER BY created_at DESC", user)
        orders = cursor.fetchall()
        if orders:
            context.user_data['orders'] = orders
            context.user_data['current_order'] = 0
            show_order(update, context)
            return MAIN_MENU
        else:
            update.message.reply_text('Sizda hali buyurtmalar yoq', reply_markup=ReplyKeyboardRemove())
            return start(update, context)
    else:
        update.message.reply_text("Ro'yxatdan o'ting", reply_markup=ReplyKeyboardRemove())
        return start(update, context)


def show_order(update: Update, context: CallbackContext) -> None:
    current_order_index = context.user_data['current_order']
    order = context.user_data['orders'][current_order_index]

    order_details = (f"Buyurtma ID: {order[0]} \n"
                     f"Suv: {order[14]} \n"
                     f"Soni: {order[3]} \n"
                     f"Manzil: {order[5]} \n"
                     f"Holati: {order[8]} \n"
                     f"Yaratilgan vaqti: {order[1]}")
    inline_keyboard = []
    if current_order_index > 0:
        inline_keyboard.append([InlineKeyboardButton('Oldingi', callback_data='prev')])
    if current_order_index < len(context.user_data['orders']) - 1:
        inline_keyboard.append([InlineKeyboardButton('Keyingi', callback_data='next')])

    reply_markup = InlineKeyboardMarkup(inline_keyboard)

    if update.callback_query:
        update.callback_query.edit_message_text(order_details, reply_markup=reply_markup)
    else:
        update.message.reply_text(order_details, reply_markup=reply_markup)


def paginate_orders(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    current_order_index = context.user_data['current_order']

    if query.data == 'next' and current_order_index < len(context.user_data['orders']) - 1:
        context.user_data['current_order'] += 1
    elif query.data == 'prev' and current_order_index > 0:
        context.user_data['current_order'] -= 1

    show_order(update, context)


def write_support(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("Sizni qiziqtirgan savolingizni yozib keting", reply_markup=ReplyKeyboardRemove())
    return SUPPORT


def save_support(update: Update, context: CallbackContext) -> int:
    user_id = update.message.from_user.id
    message = update.message.text

    cursor.execute("INSERT INTO user_contact_application (user_id, message, created_at, updated_at, is_contacted) VALUES "
                   "((SELECT id FROM users WHERE telegram_id = %s), %s, %s, %s, %s)", (user_id, message, datetime.now(), datetime.now(), False))
    conn.commit()
    update.message.reply_text('Xabaringiz qabul qilindi, siz bilan tez orada bog\'lanishadi', reply_markup=ReplyKeyboardRemove())
    return main_menu(update, context)


def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("Ro'yxatdan o'tish to'xtatildi", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def main() -> None:
    updater = Updater(env('TOKEN'))
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            PHONE: [MessageHandler(Filters.contact, phone_number)],
            NAME: [MessageHandler(Filters.text & ~Filters.command, name)],
            MAIN_MENU: [
                MessageHandler(Filters.regex('^Buyurtma berish$'), order_water),
                MessageHandler(Filters.regex('^Mening buyurtmalarim$'), my_orders),
                MessageHandler(Filters.regex("^Qo'lab quvvatlash$"), write_support),
            ],
            ORDER: [MessageHandler(Filters.text & ~Filters.command, set_order)],
            QUANTITY: [MessageHandler(Filters.text & ~Filters.command, set_quantity)],
            LOCATION: [MessageHandler(Filters.location, set_location)],
            CONFIRM: [
                MessageHandler(Filters.regex('^Tasdiqlash'), confirm_order),
                MessageHandler(Filters.regex('^Bekor qilish'), main_menu),
            ],
            SUPPORT: [MessageHandler(Filters.text & ~Filters.command, save_support)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(conv_handler)
    dispatcher.add_handler(CallbackQueryHandler(paginate_orders, pattern='^(next|prev)$'))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
