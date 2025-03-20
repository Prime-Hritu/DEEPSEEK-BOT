from pyrogram import Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from translate import Dynamic_Translate
from database.models_settings import set_ai_mode, get_ai_mode
from database.lang_settings import set_language
from translation import TEXT
from pyrogram.enums import ParseMode
from config import OWNER, FORCE
from buttons import BUTTONS
from constants import MODELS


@Client.on_callback_query()
def callback(client: Client, callback_query: CallbackQuery):
    data: str = callback_query.data
    message: Message = callback_query.message
    translator = Dynamic_Translate(message.chat.id).translate
    if data in ['about', 'help']:
        message.edit(TEXT.ABOUT if data == "about" else TEXT.HELP, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(
                    translator("<< Back"), callback_data="back-to-start")]
            ]
        ))
    elif data == "back-to-start":
        message.edit(translator(TEXT.START), reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(translator(
                "Settings ⚙️"), callback_data="setting")],
            [InlineKeyboardButton(translator("About ℹ️"), callback_data="about"),
             InlineKeyboardButton(translator("Help 🤔"), callback_data="help")],
            [InlineKeyboardButton(translator(
                "Developer 👨‍💻"), url=f"tg://user?id={OWNER.ID}")],
            [InlineKeyboardButton(translator("Updates Channel ☝️"),
                                  url=FORCE.CHANNEL_LINK)]
        ]))
    elif data == "setting" or data == "back-to-set-models":
        message.edit(translator(TEXT.SETTINGS), parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(
                    translator("Change Model 🔮"), callback_data="setmodel")],
                [InlineKeyboardButton(
                    translator("Change Language 🌐"), callback_data="setlang")],
                [InlineKeyboardButton(
                    translator("<< Back"), callback_data="back-to-start")]
            ]
        ))
    elif data == "setmodel":
        button = BUTTONS(message).INLINE()
        message.edit(translator(
            """<b>☝️ Choose between various AI models:</b>"""), reply_markup=button)

    elif data.startswith("setmodel+"):
        after = data.split("+")[1]
        if after == "v3":
            model = MODELS.DEEPSEEKV3
        elif after == "r1":
            model = MODELS.DEEPSEEKR1
        elif after == "r1_distill_qwen_14b":
            model = MODELS.DEEPSEEKR1DISTILLQWEN14B
        elif after == "r1_distill_qwen_1.5b":
            model = MODELS.DEEPSEEKR1DISTILLQWEN15B
        else:
            model = MODELS.DEEPSEEKV3
        got_mode = MODELS(get_ai_mode(message.chat.id))
        if got_mode == MODELS.NONE:
            got_mode = MODELS.DEEPSEEKV3
        if got_mode == model:
            text = "<b>❌ Model you selected was already set.</b>"
        else:
            text = "<b>✅ New model set successfully.</b>"
        set_ai_mode(message.chat.id, model)
        button = BUTTONS(message).INLINE()
        message.edit(translator(text), reply_markup=button)

    elif data == "setlang":
        board = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(
                    "🇬🇧 English", callback_data="setlang+en"),
                    InlineKeyboardButton(
                    "🇪🇸 Spanish", callback_data="setlang+es")],
                [InlineKeyboardButton(
                    "🇫🇷 French", callback_data="setlang+fr"),
                    InlineKeyboardButton(
                    "🇩🇪 German", callback_data="setlang+de")],
                [InlineKeyboardButton("🇮🇳 Hindi", callback_data="setlang+hi"),
                 InlineKeyboardButton(
                    "🇷🇺 Russian", callback_data="setlang+ru")],
                [InlineKeyboardButton(
                    "🇨🇳 Chinese", callback_data="setlang+zh"),
                    InlineKeyboardButton(
                    "🇦🇪 Arabic", callback_data="setlang+ar")],
                [InlineKeyboardButton(
                    "🇯🇵 Japanese", callback_data="setlang+ja"),
                    InlineKeyboardButton("🇰🇷 Korean", callback_data="setlang+ko")],
                [InlineKeyboardButton(
                    translator("<< Back"), callback_data="back-to-set-models")]

            ]
        )
        message.edit(translator(
            """<b>🌎 Choose your preferred language:</b>"""), reply_markup=board)

    elif data.startswith("setlang+"):
        lang = data.split("+")[1]
        set_language(message.chat.id, lang)
        translated = translator(TEXT.START)
        message.reply_text(translated, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(
            translator("<< Back"), callback_data="back-to-set-models")]]))
