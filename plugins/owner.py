from pyrogram import Client, filters
from pyrogram.types import Message
from translate import Dynamic_Translate
from translation import TEXT
from config import OWNER
from database.users import get_served_users


def broadcast(user_list: list, message: Message, msg: str):
    no_sent = 0
    no_failed = 0
    for i in user_list:
        try:
            y = i["user_id"]
            if "--f" in msg:
                try:
                    message.forward(y)
                    no_sent += 1
                except Exception:
                    no_failed += 1
                    continue
            else:
                try:
                    message.copy(y)
                    no_sent += 1
                except Exception:
                    no_failed += 1
                    continue
        except:
            no_failed += 1
            continue
    return no_sent, no_failed


@Client.on_message(filters.command("status"))
def show_status(client: Client, message: Message):
    if not int(message.chat.id) == int(OWNER.ID):
        return
    translator = Dynamic_Translate(message.chat.id).translate
    msg: Message = message.reply_text(
        translator(TEXT.FETCHING_DATABSE), reply_to_message_id=message.id
    )
    total_users = len(get_served_users())
    msg.edit(translator(TEXT.STATUS.format(total_users)))


@Client.on_message(filters.private & filters.command("broad"))
def broadcaster(c: Client, m: Message):
    if not int(m.chat.id) == int(OWNER.ID):
        return m.delete()
    translator = Dynamic_Translate(m.chat.id).translate
    m.reply_text(translator(TEXT.START), reply_to_message_id=m.id)
    msg_to_br = m.reply_to_message
    if not msg_to_br:
        return m.reply_text(translator("REPLY TO A MESSAGE !"))
    users_list = get_served_users()
    no_sent, no_failed = broadcast(users_list, msg_to_br, m.text)
    c.send_message(
        chat_id=int(OWNER.ID), text=translator(TEXT.BROADCAST.format(no_sent, no_failed))
    )
