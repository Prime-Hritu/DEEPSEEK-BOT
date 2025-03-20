from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from translate import translate_to_send
from database.models_settings import get_ai_mode
from constants import MODELS
from pyrogram.types import Message


class BUTTONS:
    def __init__(self, message: Message):
        self.message = message

    def INLINE(self):
        return InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(
                    "✅ DeepSeek V3 🐳" if get_ai_mode(self.message.chat.id) == MODELS.DEEPSEEKV3.value or get_ai_mode(self.message.chat.id) == None else "DeepSeek V3 🐳", callback_data="setmodel+v3"),
                    InlineKeyboardButton(
                    "✅ DeepSeek-R1 🐳" if get_ai_mode(self.message.chat.id) == MODELS.DEEPSEEKR1.value else "DeepSeek-R1 🐳", callback_data="setmodel+r1")
                 ],
                [InlineKeyboardButton(
                    "✅ DeepSeek-R1-Distill-Qwen-14B 🐳" if get_ai_mode(self.message.chat.id) == MODELS.DEEPSEEKR1DISTILLQWEN14B.value else "DeepSeek-R1-Distill-Qwen-14B 🐳", callback_data="setmodel+r1_distill_qwen_14b"
                )],
                [InlineKeyboardButton(
                    "✅ DeepSeek-R1-Distill-Qwen-1.5B 🐳" if get_ai_mode(self.message.chat.id) == MODELS.DEEPSEEKR1DISTILLQWEN15B.value else "DeepSeek-R1-Distill-Qwen-1.5B 🐳", callback_data="setmodel+r1_distill_qwen_1.5b"
                )],
                [InlineKeyboardButton(
                    translate_to_send("<< Back", self.message.chat.id), callback_data="back-to-set-models")]
            ]
        )
