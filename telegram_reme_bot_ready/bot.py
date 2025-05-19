from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, filters
from pymongo import MongoClient

# GANTI DENGAN TOKEN BOT KAMU
TOKEN = 'ISI_TOKEN_BOT_KAMU'
# GANTI DENGAN URI MONGODB KAMU
MONGO_URI = 'ISI_MONGODB_URI_KAMU'

client = MongoClient(MONGO_URI)
db = client['remebot']
users = db['users']

# /reg
async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    username = update.effective_user.username or update.effective_user.first_name

    if users.find_one({'user_id': user_id}):
        await update.message.reply_text("❗ Kamu sudah terdaftar.")
    else:
        users.insert_one({'user_id': user_id, 'username': username, 'coin': 100})
        await update.message.reply_text(f"✅ Registrasi berhasil, {username}! Coin awal: 100")

# /cekcoin
async def cekcoin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = users.find_one({'user_id': user_id})
    if not user:
        await update.message.reply_text("❗ Kamu belum terdaftar. Gunakan /reg terlebih dahulu.")
    else:
        await update.message.reply_text(f"💰 Coin kamu: {user['coin']}")

# Menjalankan bot
if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("reg", register, filters=filters.ALL))
    app.add_handler(CommandHandler("cekcoin", cekcoin, filters=filters.ALL))

    print("✅ Bot berjalan...")
    app.run_polling()
