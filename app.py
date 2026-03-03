from fastapi import FastAPI, Request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from config import BOT_TOKEN, ADMIN_ID
from database import init_db

app = FastAPI()
application = Application.builder().token(BOT_TOKEN).build()

# رسالة البداية
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("السنة الأولى", callback_data="year_1")],
        [InlineKeyboardButton("السنة الثانية", callback_data="year_2")],
        [InlineKeyboardButton("السنة الثالثة", callback_data="year_3")]
    ]

    await update.message.reply_text(
        "انا استاذك الخاص الذكي . يسرنا انك وضعت ثقتك بي خلال رحلتك في الثانوية استمتع😁",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# معالجة الأزرار
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    if data.startswith("year"):
        keyboard = [
            [InlineKeyboardButton("الفصل الأول", callback_data=f"{data}_ch1")],
            [InlineKeyboardButton("الفصل الثاني", callback_data=f"{data}_ch2")],
            [InlineKeyboardButton("الفصل الثالث", callback_data=f"{data}_ch3")],
            [InlineKeyboardButton("رجوع", callback_data="back_main")]
        ]

        await query.edit_message_text(
            "اختر الفصل:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif data == "back_main":
        await start(update, context)

# Webhook
@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, application.bot)
    await application.process_update(update)
    return {"ok": True}

application.add_handler(CommandHandler("start", start))
application.add_handler(CallbackQueryHandler(button_handler))

init_db()
