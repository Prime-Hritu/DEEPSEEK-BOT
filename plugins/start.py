from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from translate import Dynamic_Translate
from database.users import add_served_user
from translation import TEXT
from config import OWNER, FORCE, BOT


@Client.on_message(filters.command("start"))
def start(client: Client, message: Message):
    add_served_user(message.chat.id)
    translator = Dynamic_Translate(message.chat.id).translate
    message.reply_text(translator(TEXT.START), reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton(translator(
            "Settings ⚙️"), callback_data="setting")],
        [InlineKeyboardButton(translator("About ℹ️"), callback_data="about"),
         InlineKeyboardButton(translator("Help 🤔"), callback_data="help")],
        [InlineKeyboardButton(translator(
            "Developer 👨‍💻"), url=f"tg://user?id={OWNER.ID}")],
        [InlineKeyboardButton(translator("Updates Channel ☝️"),
                              url=FORCE.CHANNEL_LINK)],
        [InlineKeyboardButton(translator("Source Code ↗️"),
                              url=BOT.SOURCE)]
    ]))
