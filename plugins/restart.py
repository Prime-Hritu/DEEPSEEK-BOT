from pyrogram import Client, filters
from pyrogram.types import Message
from translate import Dynamic_Translate
from database.users import add_served_user
from database.ai_db import delete_chat


@Client.on_message(filters.command("restart"))
def restart(client: Client, message: Message):
    add_served_user(message.chat.id)
    translator = Dynamic_Translate(message.chat.id).translate
    delete_chat(message.chat.id)
    message.reply_text(translator("""Chat restarted successfully"""))
