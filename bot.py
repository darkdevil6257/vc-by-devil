from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters
from elevenlabs.client import ElevenLabs
import os

TELEGRAM_BOT_TOKEN = "7983931203:AAE9B5Blt6QFNLyzto-m-NA4rxzhZAnySU8"
ELEVENLABS_API_KEY = "sk_0ce2cd068789ab88004f409ac438a7e6262f9e2fd1132f1d"
VOICE_ID = "TRnaQb7q41oL7sV0w6Bu"

client = ElevenLabs(
    api_key=ELEVENLABS_API_KEY
)

async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:

        voice = update.message.voice

        tg_file = await context.bot.get_file(voice.file_id)

        input_path = "input.ogg"

        await tg_file.download_to_drive(input_path)

        audio_file = open(input_path, "rb")

        response = client.speech_to_speech.convert(
            voice_id=VOICE_ID,
            audio=audio_file,
            model_id="eleven_multilingual_sts_v2"
        )

        output_path = "output.mp3"

        with open(output_path, "wb") as f:
            for chunk in response:
                f.write(chunk)

        await update.message.reply_voice(
            voice=open(output_path, "rb")
        )

        audio_file.close()

        os.remove(input_path)
        os.remove(output_path)

    except Exception as e:
        print(e)
        await update.message.reply_text(
            f"Error: {e}"
        )

app = Application.builder().token(
    TELEGRAM_BOT_TOKEN
).build()

app.add_handler(
    MessageHandler(filters.VOICE, handle_voice)
)

print("Bot Running...")

app.run_polling()
