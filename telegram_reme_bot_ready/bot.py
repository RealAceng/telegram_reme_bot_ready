import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, filters
from pymongo import MongoClient
from keep_alive import keep_alive  # Tambahkan ini

# Ambil dari environment variable
TOKEN = "7599418730:AAF6xghU68dBFfm2AD-OdjApqMC3vhS6XNY"  # Ganti dengan token bot Anda
MONGO_URI = "mongodb+srv://megawatisimbolan:Aceng123.@cluster0.ionguub.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"  # Ganti dengan URI MongoDB Anda

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
    keep_alive()  # Aktifkan server kecil agar bisa diping UptimeRobot

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("reg", register, filters=filters.ALL))
    app.add_handler(CommandHandler("cekcoin", cekcoin, filters=filters.ALL))

    print("✅ Bot berjalan...")
    app.run_polling()
