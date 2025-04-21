
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp

BOT_TOKEN = "7721653542:AAFzLQ1sL1AxJyXTcVAklvcnGUw19XoFVqo"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Gửi link Twitter để tải video nhé!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if "twitter.com" not in url:
        await update.message.reply_text("Vui lòng gửi link Twitter hợp lệ.")
        return

    ydl_opts = {
        'outtmpl': 'video.%(ext)s',
        'format': 'best',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=True)
            video_file = ydl.prepare_filename(info)
            await update.message.reply_video(video=open(video_file, 'rb'))
            os.remove(video_file)
        except Exception as e:
            await update.message.reply_text(f"Lỗi: {e}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("Bot is running...")
    app.run_polling()
