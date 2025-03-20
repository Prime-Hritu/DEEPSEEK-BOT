from pyrogram import Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from translate import Dynamic_Translate
from database.users import add_served_user
from database.members import add_members_id
from translation import TEXT
from database.models_settings import get_ai_mode
from deepseek import DEEPSEEK
from constants import MODELS
from pyrogram.types import Message, ChatMember, Chat
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import UserNotParticipant
from config import FORCE as FORCER


@Client.on_message()
def chat(client: Client, message: Message):
    add_served_user(message.chat.id)
    translator = Dynamic_Translate(message.chat.id).translate
    if FORCER.FORCE_BOOL == True:
        FORCE = False
        try:
            got_chat_member: ChatMember = Client.get_chat_member(
                FORCER.CHANNEL_USERNAME, message.chat.id
            )
            if not got_chat_member.status in [
                ChatMemberStatus.OWNER,
                ChatMemberStatus.ADMINISTRATOR,
                ChatMemberStatus.MEMBER,
            ]:
                FORCE = True
        except UserNotParticipant:
            FORCE = True
        if FORCE == True:
            chat: Chat = Client.get_chat(FORCER.CHANNEL_USERNAME)
            chat_title = chat.title
            add_members_id(message.chat.id)
            return message.reply_photo(
                photo="./images/tg.jpg",
                caption=translator(TEXT.FORCE_SUB_TEXT.format(
                    FORCER.CHANNEL_LINK, chat_title)),
                reply_markup=InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton(
                            translator("🔈 Join Channel"), url=FORCER.CHANNEL_LINK)],
                    ],
                ),
            )
    msg: Message = message.reply_text(translator(
        "<i>thinking...</i>"))
    query = message.text
    model = get_ai_mode(message.chat.id)
    mode = MODELS(model)
    if mode == MODELS.NONE:
        mode = MODELS.DEEPSEEKV3
    response = DEEPSEEK().huggingface(query, message.chat.id, mode)
    msg.edit(translator(response), reply_markup=InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(
                translator("<< Back to start"), callback_data="back-to-start")]
        ]
    ))
