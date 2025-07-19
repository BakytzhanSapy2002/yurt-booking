from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from sheets_api import get_availability, add_booking, list_bookings, delete_booking_by_id, get_next_available, edit_booking
from datetime import timedelta
from telegram import Update

# Telegram ID – тек админ қолдана алады
ADMIN_ID = 1316179678  # <-- Өз ID-ңызды жазыңыз

BOT_TOKEN = "7462800568:AAFu2y3_znZkg1wviHyKwEcuTBlgWkFpWCg"
def get_help_text(user_id):
    if user_id == ADMIN_ID:
        return (
            "Сәлем, админ! 😊\n\n"
            "🛠 *Админ командалары*:\n"
            "/add\\_booking Yurt1 2025-07-15\\_14:00 2025-07-15\\_18:00 Айгүл +77001234567 Туған күнге – бронь қосу\n"
            "/delete\\_booking 2 – ID арқылы бронь жою\n"
            "/edit\\_booking 2 – ID арқылы броньды өңдеу\n"
            "/list\\_bookings – барлық броньдарды көру\n"
            "/next\\_available – келесі бос уақыттар\n"
            "/availability – барлық броньдар\n"
        )
    else:
        return (
            "Сәлем! Бұл – Киіз Үй Брондау Бот 😊\n\n"
            "📦 Қол жетімді командалар:\n"
            "/availability – броньдар тізімі\n"
            "/next\\_available – келесі бос уақытты көру\n"
            "/request\\_booking – бронь сұрау\n"
            "/help – көмек мәзірі\n\n"
            "Бронь жасау үшін бізге хабарласыңыз: \\+7 700 123 45 67"
        )
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = get_help_text(user_id)
    await update.message.reply_text(text, parse_mode="Markdown")
async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = get_help_text(user_id)
    await update.message.reply_text(text, parse_mode="Markdown")
async def availability(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = get_availability()
    await update.message.reply_text(text)
async def add_booking_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id != ADMIN_ID:
        await update.message.reply_text("❌ Сізде бұл команданы орындауға рұқсат жоқ.")
        return

    try:
        args = context.args
        yurt = args[0]
        start = args[1].replace("_", " ")
        end = args[2].replace("_", " ")
        name = args[3]
        phone = args[4]
        notes = " ".join(args[5:]) if len(args) > 5 else ""
        add_booking(yurt, start, end, name, phone, notes)
        await update.message.reply_text("✅ Бронь сәтті қосылды!")
    except Exception as e:
        await update.message.reply_text(f"❌ Қате: {e}\nПішім:\n/add_booking Yurt1 2025-07-15_14:00 2025-07-15_18:00 Айгүл +77001234567 Туған күнге")
async def delete_booking_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id != ADMIN_ID:
        await update.message.reply_text("❌ Сізде бұл команданы орындауға рұқсат жоқ.")
        return

    try:
        booking_id = context.args[0]
        result = delete_booking_by_id(booking_id)
        if result:
            await update.message.reply_text("✅ Бронь жойылды.")
        else:
            await update.message.reply_text("❌ Мұндай ID табылмады.")
    except Exception as e:
        await update.message.reply_text(f"Қате: {e}\nПішім:\n/delete_booking 2")
async def list_bookings_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id != ADMIN_ID:
        await update.message.reply_text("❌ Бұл команданы тек админ қолдана алады.")
        return

    text = list_bookings()
    await update.message.reply_text(text)
async def next_available_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = get_next_available()
    await update.message.reply_text(text)
async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    if user_id == ADMIN_ID:
        text = (
            "🛠 *Админ командалары*:\n\n"
            "/add_booking Yurt1 2025-07-15_14:00 2025-07-15_18:00 Айгүл +77001234567 Туған күнге – бронь қосу\n"
            "/delete_booking 2 – ID арқылы бронь жою\n"
            "/list_bookings – барлық броньдарды көру\n"
            "/edit\\_booking 2 – ID арқылы броньды өңдеу\n"
            "/next_available – келесі бос уақыттар\n"
            "/availability – барлық броньдар\n"
        )
    else:
        text = (
            "👋 Қош келдіңіз! Бұл Киіз Үй Брондау Бот.\n\n"
            "📦 Қол жетімді командалар:\n"
            "/start – ботты бастау\n"
            "/availability – броньдар тізімі\n"
            "/next_available – келесі бос уақытты көру\n"
            "/help – осы көмек мәзірі\n\n"
            "Егер сізге бронь жасау қажет болса, бізге хабарласыңыз: +7 700 123 45 67"
        )

    await update.message.reply_text(text, parse_mode="Markdown")
async def request_booking_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        args = context.args
        if len(args) < 6:
            raise ValueError("Пішім қате")

        yurt = args[0]
        start = args[1].replace("_", " ")
        end = args[2].replace("_", " ")
        name = args[3]
        phone = args[4]
        notes = " ".join(args[5:])

        # Қолданушы мәліметтері
        user = update.message.from_user
        requester = f"{user.first_name} (@{user.username})" if user.username else user.first_name

        message = (
            f"📥 *Жаңа бронь сұранысы!*\n\n"
            f"👤 Қолданушы: {requester}\n"
            f"🏕 Киіз үй: {yurt}\n"
            f"📅 Күндер: {start} – {end}\n"
            f"👤 Есімі: {name}\n"
            f"📞 Тел: {phone}\n"
            f"📝 Комментарий: {notes}\n"
        )

        # 1. Қолданушыға растау
        await update.message.reply_text("✅ Сұранысыңыз қабылданды. Админ сізбен жақында хабарласады!")

        # 2. Админге жолдау
        await context.bot.send_message(chat_id=ADMIN_ID, text=message, parse_mode="Markdown")

    except Exception as e:
        await update.message.reply_text(
            f"❌ Қате: {e}\n\n"
            "Пайдалану мысалы:\n"
            "/request_booking Yurt1 2025-07-15_14:00 2025-07-15_18:00 Нұрлан +77001112233 Достармен демалыс"
        )
async def edit_booking_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id != ADMIN_ID:
        await update.message.reply_text("❌ Сізде бұл команданы орындауға рұқсат жоқ.")
        return

    try:
        args = context.args
        if len(args) < 3:
            raise ValueError("Пішім қате")

        booking_id = args[0]
        field = args[1]
        new_value = " ".join(args[2:]).replace("_", " ")

        allowed_fields = ["Yurt", "StartDate", "EndDate", "ClientName", "Phone", "Notes"]
        if field not in allowed_fields:
            await update.message.reply_text("❌ Қате: Мұндай өріс жоқ. Төмендегі өрістерді ғана өзгерте аласыз:\n" + ", ".join(allowed_fields))
            return

        result = edit_booking(booking_id, field, new_value)
        if result:
            await update.message.reply_text("✅ Өзгеріс сәтті жасалды.")
        else:
            await update.message.reply_text("❌ Мұндай ID табылмады.")
    except Exception as e:
        await update.message.reply_text(
            f"Қате: {e}\n"
            "Пайдалану мысалы:\n"
            "/edit_booking 3 Phone +77009998877"
        )
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("availability", availability))
app.add_handler(CommandHandler("add_booking", add_booking_handler))
app.add_handler(CommandHandler("delete_booking", delete_booking_handler))
app.add_handler(CommandHandler("edit_booking", edit_booking_handler))
app.add_handler(CommandHandler("list_bookings", list_bookings_handler))
app.add_handler(CommandHandler("next_available", next_available_handler))
app.add_handler(CommandHandler("help", help_handler))
app.add_handler(CommandHandler("request_booking", request_booking_handler))

app.run_polling()