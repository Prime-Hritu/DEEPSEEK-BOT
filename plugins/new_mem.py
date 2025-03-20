from pyrogram import Client
from pyrogram import filters
from database import MONGO, check_mongo
from database.members import get_all_members_ids, remove_members_id
from pyrogram.types import ChatMemberUpdated
from config import FORCE


@Client.on_chat_member_updated(filters.user(get_all_members_ids()))
def handle_member_update(client: Client, update: ChatMemberUpdated):
    if (
        update.new_chat_member
        and not update.old_chat_member
        and MONGO.URI
        and FORCE.FORCE_BOOL == True
    ):
        if not check_mongo() == False:
            try:
                remove_members_id(update.from_user.id)
            except:
                pass
            client.send_photo(
                chat_id=update.from_user.id,
                photo="./images/thanks.jpg",
                caption="<b>Thanks for joining <a href='{}'>our channel</a></b>".format(FORCE.CHANNEL_LINK),
            )
            