from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from translate import Dynamic_Translate
from database.users import add_served_user
from translation import TEXT
from pyrogram.enums import ParseMode


@Client.on_message(filters.command("settings"))
def settings(client: Client, message: Message):
    add_served_user(message.chat.id)
    translator = Dynamic_Translate(message.chat.id).translate
    message.reply_text(translator(TEXT.SETTINGS), parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(
                translator("Change Model 🔮"), callback_data="setmodel")],
            [InlineKeyboardButton(
                translator("Change Language 🌐"), callback_data="setlang")],
            [InlineKeyboardButton(
                translator("<< Back to start"), callback_data="back-to-start")]
        ]
    ))
