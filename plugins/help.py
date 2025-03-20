from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from translate import Dynamic_Translate
from database.users import add_served_user
from translation import TEXT
from pyrogram.enums import ParseMode


@Client.on_message(filters.command("help"))
def help(client: Client, message: Message):
    translator = Dynamic_Translate(message.chat.id).translate
    add_served_user(message.chat.id)
    message.reply_text(translator(TEXT.HELP), parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(
                translator("<< Back to start"), callback_data="back-to-start")]
        ]
    ))
