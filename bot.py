import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = "7939139664:AAFuUPG16jhViemqpClxIMlk-U2gLhohemg"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send me a TikTok link and I'll download the video!")

async def download_tiktok(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text

    if "tiktok.com" not in url:
        await update.message.reply_text("❌ Please send a valid TikTok link.")
        return

    await update.message.reply_text("⏳ Downloading...")

    try:
        api_url = f"https://tikwm.com/api/?url={url}"
        response = requests.get(api_url).json()

        if response["code"] == 0:
            video_url = response["data"]["play"]
            await context.bot.send_video(chat_id=update.effective_chat.id, video=video_url)
        else:
            await update.message.reply_text("⚠️ Failed to get video. Try another link.")

    except Exception as e:
        await update.message.reply_text("⚠️ Error downloading video.")
        print("Error:", e)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_tiktok))

    print("Bot is running...")
    app.run_polling()
